import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import io
import random
import sqlite3

import time
import yaml
from pathlib import Path
import os
from controllers import log



# read yaml
def read_yaml(yamlfile):
    """expects path/file"""
    try:
        with open(str(yamlfile), "r", encoding = "utf-8") as fyamlfile:
            return yaml.safe_load(fyamlfile)
    except IOError as errio:
        log.error("Can't find %s.", yamlfile)
        #raise errio
        raise SystemExit(3)
    except yaml.parser.ParserError as errparse:
        log.error("ParserError in %s.", yamlfile)
        #raise errparse
        raise SystemExit(3)
    except yaml.scanner.ScannerError as errscan:
        log.error("ScannerError in %s.", yamlfile)
        #raise errscan
        raise SystemExit(3)
    except Exception as err:
        log.error(" trying to load %s.", yamlfile)
        raise err
        raise SystemExit(3)


def string_to_list(string_list):
    
    number_list = []
    try:
        for letter in string_list:
            if letter.isnumeric():
                number_list.append(int(letter))
    except:
        pass
    
    finally:
        return number_list

    
def convertToBinaryData(image_name):
        #Convert digital data to binary format
        if image_name == "" or image_name == "-":
            img = Image.new('RGB', (200, 200), random_rgb())
            with io.BytesIO() as output:
                img.save(output, format="JPEG")
                blobData = output.getvalue()
            return blobData
        else:
            try:
                with open(image_name, 'rb') as file:
                    blobData = file.read()
                log.debug("UTILS: Successfully reading Image")
                return blobData
            except:
                log.error("UTILS: Reading Image failed")    
                return ""


def binary_to_image(blobData):
    if blobData == "" or blobData == "-":
        img = Image.new('RGB', (500, 1080), random_rgb())
        return img
    else:
        return Image.open(io.BytesIO(blobData))


def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))


def string_unify(db_name):
    new_db_name = db_name.replace(" ", "_")
    return new_db_name.lower()


def open_file_dialog(file_type):
    file_types = []
    if file_type == "image":
        file_types.append(("jpeg files","*.jpg"))
        file_types.append(("png files", "*.png"))
    elif file_type == "database":
        file_types.append(("DB files","*.db"))
    elif file_type == "excel_csv":
        file_types.append(("CSV files","*.csv"))
        file_types.append(("Excel 2010 files","*.xlsx"))
    elif file_type == "text":
        file_types.append(("PDF files","*.pdf"))
        file_types.append(("TXT files","*.txt"))
        file_types.append(("Word 2010 files","*.docx"))
    
    file_types.append(("all files","*.*"))

    filename = filedialog.askopenfilename(initialdir = "/data",title = "Select file",filetypes = tuple(file_types))
    return filename 


def random_rgb():
    return (random.randint(0,170), random.randint(0,170), random.randint(0,170))


class Config():
    def __init__(self):
        lct_lib = Path(os.path.dirname(os.path.abspath(__file__)))
        self.lct_root = lct_lib.parents[0]
        log.info("Config.lct_root: {}".format(self.lct_root))
        self.check_config_integrity()
        self.conf = read_yaml( self.lct_root / "config.yaml")
        self.check_db_integrity(self.conf["word_attributes"], self.conf["vocabulary_metadata"])
        try:
            self.log_level = self.conf["log_level"]
            log.info("config.yaml entry log_level is {}.".format(self.log_level))
        except:
            self.log_level = "WARNING"
            log.warn("config.yaml entry log_level not set, set Default Level.")
        log.handlers[0].setLevel(self.log_level)

    def _get_config_entry(self, yaml_key, optional = True):
        if optional:
            try:
                if self.conf[yaml_key] == '':
                    value = ''
                    log.error("config.yaml entry {} is empty.".format(yaml_key))
                else:
                    value = self.conf[yaml_key]
                    log.info("config.yaml entry {} is set.".format(yaml_key))
            except KeyError:
                value = ''
                log.info("config.yaml entry {} is missing.".format(yaml_key))
            return value
        else:
            try: # essential settings entries should error and exit
                value = self.conf[yaml_key]
            except KeyError as ke:
                log.error("Missing essential entry in config.yaml: {}".format(ke))
                raise SystemExit(3)
            return value
    

    def check_config_integrity(self):
        if not os.path.exists('data'):
            os.makedirs('data')

        if not os.path.isfile("config.yaml"): 
            log.info("Creating config.yaml")
            config_str = '''log_level: WARNING
part_of_speech: [Noun, Verb, Adjective, Adverb, Pronoun, Preposition, Conjunction, Interjection, Article]
word_attributes: [word_id, transliteration, phonetics, pos, translation, example_sentence, example_translation, description, related_image]
vocabulary_metadata: [name, author, language, notes]
start_db: "data/start.db"
consonants: [c,z,x,s,d,f,v,w,g,k,b,p,m,n,h,j]
special_vowels: [ä,ö,ü,è]
vowels: [a,e,i,o,u]
construction_config: 
              "width" : 4 
              "height" : 30
scraper_websites:
              - "https://1000mostcommonwords.com/"'''

            with open("config.yaml", 'w', encoding="utf-8") as config_file:
                config_file.write(config_str)
        else:
            pass
    

    def check_db_integrity(self, headings, metaheadings):

        if not os.path.isfile("data/start.db"):
            binary_image = convertToBinaryData("ressources/related_images/1.jpg")

            sql_create_db = '''CREATE TABLE VOCABULARY
                                        ({} INTEGER PRIMARY KEY,
                                            {} varchar(255) NOT NULL,
                                            {} varchar(255) NOT NULL,
                                            {} TEXT NOT NULL,
                                            {} varchar(255) NOT NULL,
                                            {} TEXT NOT NULL,
                                            {} TEXT NOT NULL,
                                            {} TEXT NOT NULL,
                                            {} BLOB NOT NULL)'''.format(*headings)

            sql_create_meta = ''' CREATE TABLE METADATA
                                ({} varchar(255),
                                {} varchar(255),
                                {} varchar(255),
                                {} TEXT)'''.format(*headings)
            
            conn = sqlite3.connect('data/start.db')
            c = conn.cursor()
            c.execute(sql_create_db)
            c.execute(sql_create_meta)

            sql_insertion_query = '''INSERT INTO VOCABULARY ({},{},{},{},{},{},{},{})
                                            VALUES (?,?,?,?,?,?,?,?)'''.format(*headings[1:])

            sql_vocab_data = ('Welcome',
                        '/ˈwelkəm/',
                        'Adjective',
                        "willkommen",
                        "You are very welcome here.", 
                        "Du bist hier sehr willkommen.",
                        '''<p><b>This tool is designed to help you construct languages.</b> </p>
Up to date its main function is to manage vocabulary, and secondly to form words. It should not be confused with a language generator.
Best practices and usage examples can be found in the <a href="https://github.com/schobernoise/Language-Construction-Tool">documentation</a>.''', 
                        binary_image)
            
            sql_meta_query = '''INSERT INTO METADATA VALUES(?,?,?,?)'''
            sql_meta_content=("Start DB", "Fabian Schober", "German", "This is the tutorial Database.")

            c.execute(sql_insertion_query, sql_vocab_data)
            c.execute(sql_meta_query, sql_meta_content)
            conn.commit()
            conn.close()

    
    



    


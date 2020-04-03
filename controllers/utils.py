import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import io

import time
import yaml
from pathlib import Path
import os
from controllers import log


# read yaml
def read_yaml(yamlfile):
    """expects path/file"""
    try:
        with open(str(yamlfile), "r") as fyamlfile:
            return yaml.load(fyamlfile, Loader=yaml.SafeLoader)
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
    

def convertToBinaryData(image_name):
        #Convert digital data to binary format
        if image_name == "":
            return ""
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
    if blobData == "":
        img = Image.new('RGB', (500, 1080), (228, 150, 150))
        return img
    else:
        return Image.open(io.BytesIO(blobData))



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
    
    file_types.append(("all files","*.*"))

    filename = filedialog.askopenfilename(initialdir = "/data",title = "Select file",filetypes = tuple(file_types))
    return filename 


class Config():
    def __init__(self):
        lct_lib = Path(os.path.dirname(os.path.abspath(__file__)))
        self.lct_root = lct_lib.parents[0]
        log.info("Config.lct_root: {}".format(self.lct_root))
        self.conf = read_yaml( self.lct_root / "config.yaml")
        try: 
            self.log_level = self.conf["log_level"]
            log.info("config.yaml entry log_level is {}.".format(self.log_level))
        except:
            self.log_level = "WARNING"
            log.warn("config.yaml entry log_level not set, set Default Level.")



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
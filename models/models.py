from controllers import utils
from controllers import log
import sqlite3
from PIL import Image
import io

class voc_model():
    def __init__(self, conf):
        self.word_attribute_headings = conf.conf["word_attributes"]
        self.metadata_headings = conf.conf["vocabulary_metadata"]
        self.pos_list = conf.conf["part_of_speech"]


    def load_db(self, db_file="", metadata=[], mode="load"):
        if db_file=="":
            db_file = self.db_file
        else:
            self.db_file = db_file

        conn = sqlite3.connect(db_file)
        self.vocabulary = []

        if mode == "create":
            sql_create_voc = '''CREATE TABLE VOCABULARY
                                ({} INTEGER PRIMARY KEY,
                                {} varchar(255) NOT NULL,
                                {} varchar(255) NOT NULL,
                                {} TEXT NOT NULL,
                                {} varchar(255) NOT NULL,
                                {} TEXT NOT NULL,
                                {} TEXT NOT NULL,
                                {} TEXT NOT NULL,
                                {} BLOB NOT NULL)'''.format(*self.word_attribute_headings)
            

            sql_create_meta = ''' CREATE TABLE METADATA
                                ({} varchar(255),
                                {} varchar(255),
                                {} varchar(255),
                                {} TEXT)'''.format(*self.metadata_headings)

            
            sql_insert_meta = '''INSERT INTO METADATA VALUES(?,?,?,?)'''
            

            c = conn.cursor()
            c.execute(sql_create_voc)
            c.execute(sql_create_meta)
            c.execute(sql_insert_meta, tuple(metadata))
            conn.commit()

            # METADATA ASSIGNMENT

            self.metadata = {}

            for i, heading in enumerate(self.metadata_headings):
                self.metadata[heading] = metadata[i]
            
        elif mode =="load":
            sql_load_voc = "SELECT * FROM VOCABULARY"
            c = conn.cursor()
            c.execute(sql_load_voc)

            rows = c.fetchall()
            conn.commit()
            for row in rows:
                word_args = {}
                for i, value in enumerate(row):
                    if self.word_attribute_headings[i] == "related_image":
                        word_args[self.word_attribute_headings[i]] = utils.binary_to_image(value)
                    else:
                        word_args[self.word_attribute_headings[i]] = value

                # print(word_args)
                self.vocabulary.append(word(**word_args))

            sql_load_meta = "SELECT * FROM METADATA"
            
            c = conn.cursor()
            c.execute(sql_load_meta)
            rows = c.fetchall()
            conn.commit()

            self.metadata = {}
            for i, heading in enumerate(self.metadata_headings):
                self.metadata[heading] = rows[0][i]


    def update_word(self, form_contents, word_id):
        conn = sqlite3.connect(self.db_file)
        try:
            log.debug("MODEL: Updated Word ID {}".format(word_id))
            for key, value in form_contents.items():
                sql_update_word = '''UPDATE VOCABULARY SET {} = ? WHERE word_id == ?'''.format(key)
                c = conn.cursor()
                c.execute(sql_update_word, (value, word_id))
                conn.commit()
        except:
            log.error("MODEL: Updating Word ID {} failed".format(word_id))
         
        self.load_db()

    
    def update_vocabulary_metadata(self, form_contents):
        conn = sqlite3.connect(self.db_file)
        try:
            log.debug("MODEL: Updated Vocabulary Metadata.")
            for key, value in form_contents.items():
                sql_update_word = '''UPDATE METADATA SET {} = ?'''.format(key)
                c = conn.cursor()
                c.execute(sql_update_word, (value,))
                conn.commit()
        except:
            log.error("MODEL: Updating Vocabulary Metadata failed")
         
        self.load_db()
    
        
    
    def save_word(self, form_contents):
        sql_insert_word_values = []

        for key, value in form_contents.items():
            sql_insert_word_values.append(value)


        sql_insert_new_word = '''INSERT INTO VOCABULARY ({},{},{},{},{},{},{},{})
                                VALUES (?,?,?,?,?,?,?,?)'''.format(*self.word_attribute_headings[1:])
    
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            c.execute(sql_insert_new_word, tuple(sql_insert_word_values))
            conn.commit()
            log.debug("MODEL: Inserted New Word in DB.")
        except:
            log.error("MODEL: Inserting Word failed")

        self.load_db()
    

    def import_words_from_file(self, import_dict):
        
        sql_import_word = '''INSERT INTO VOCABULARY ({},{},{},{},{},{},{},{})
                        VALUES (?,?,?,?,?,?,?,?)'''.format(*self.word_attribute_headings[1:])
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        word_values = []

        for imp_word in import_dict:
            temp_list = []
            for heading in self.word_attribute_headings:
                if heading != "word_id":
                    try:
                        temp_list.append(imp_word[heading])
                    except:
                        temp_list.append("-")

            word_values.append(tuple(temp_list))

        print(word_values)

        # c.executemany(sql_import_word, word_values)
        # conn.commit()
        try:
            c.executemany(sql_import_word, word_values)
            conn.commit()
            log.debug("MODEL: Imported Word from File")
        except:
            log.error("MODEL: Importing Word from File failed")
         
        self.load_db()

    
    def delete_word(self, word_id):
        # print(word_id)
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        sql_del_word = '''DELETE FROM VOCABULARY WHERE [word_id] = ?'''

        try:
            c.execute(sql_del_word, (word_id,))
            conn.commit()
            log.debug("MODEL: Deleted Word ID {word_id} from DB.")
        except:
            log.error("MODEL: Deleting Word ID {word_id} failed")
         
        self.load_db()
    
    
    def populate_database(self, population_words):
        temp_words = []
        for word in population_words:
            temp_words.append(("-","-","-",word,"-","-","-","-"))

        sql_populate_db = '''INSERT INTO VOCABULARY ({},{},{},{},{},{},{},{})
                        VALUES (?,?,?,?,?,?,?,?)'''.format(*self.word_attribute_headings[1:])
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        try:
            c.executemany(sql_populate_db, temp_words)
            conn.commit()
            log.debug("MODEL: Successfully populated Database.")
        except:
            log.error("MODEL: Failed populating Database.")
        
        self.load_db()



class word():
    def __init__(self, **kwargs):
        self.attributes = {}
        for key, value in kwargs.items():
            self.attributes[key] = value
    




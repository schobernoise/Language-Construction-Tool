from controllers import utils
from controllers import log
import sqlite3
from PIL import Image
import io

class voc_model():
    def __init__(self):
        pass

    def load_db(self, db_file="", metadata=[], mode="load"):
        if db_file=="":
            db_file = self.db_file
        else:
            self.db_file = db_file

        conn = sqlite3.connect(db_file)
        self.vocabulary = []

        if mode == "create":
            sql_create_voc = '''CREATE TABLE VOCABULARY
                                ([word_id] INTEGER PRIMARY KEY,
                                [word] varchar(255) NOT NULL,
                                [phonetics] varchar(255) NOT NULL,
                                [translation] TEXT NOT NULL,
                                [pos] varchar(255) NOT NULL,
                                [example_sentence] TEXT NOT NULL,
                                [example_translation] TEXT NOT NULL,
                                [description] TEXT NOT NULL,
                                [related_image] BLOB NOT NULL)'''

            sql_create_meta = ''' CREATE TABLE METADATA
                                ([name] varchar(255),
                                [author] varchar(255),
                                [language] varchar(255),
                                [notes] TEXT)'''

            
            sql_insert_meta = '''INSERT INTO METADATA VALUES(?,?,?,?)'''
            

            c = conn.cursor()
            c.execute(sql_create_voc)
            c.execute(sql_create_meta)
            c.execute(sql_insert_meta, tuple(metadata))
            conn.commit()

            self.metadata = {
                            "name": metadata[0],
                            "author": metadata[1],
                            "language": metadata[2],
                            "notes": metadata[3]
                        }

            
        elif mode =="load":
            sql_load_voc = "SELECT * FROM VOCABULARY"
            c = conn.cursor()
            c.execute(sql_load_voc)

            rows = c.fetchall()
            conn.commit()
            for row in rows:
                self.vocabulary.append(word(
                    word_id = row[0],
                    word = row[1],
                    phonetics = row[2],
                    pos = row[3],
                    translation = row[4],
                    example_sentence = row[5],
                    example_translation = row[6],
                    description = row[7],
                    related_image = utils.binary_to_image(row[8])
                ))

            sql_load_meta = "SELECT * FROM METADATA"
            
            c = conn.cursor()
            c.execute(sql_load_meta)
            rows = c.fetchall()
            conn.commit()

            self.metadata = {
                        "name": rows[0][0],
                        "author": rows[0][1],
                        "language": rows[0][2],
                        "notes": rows[0][3]
                    }

    
    def update_word(self, id, column, value):

        conn = sqlite3.connect(self.db_file)
        sql_update_word = '''UPDATE VOCABULARY SET {} = ? WHERE word_id == ?'''.format(column)
        c = conn.cursor()

        try:
            c.execute(sql_update_word, (value, id))
            conn.commit()
            log.debug("MODEL: Updated Word ID {}, column {}, {}".format(id, column, value))
        except:
            log.error("MODEL: Updating Word ID {} failed".format(id))
         
        self.load_db()
        
    
    def save_word(self, form_contents):
        sql_insert_word_values = []

        sql_insert_new_word = '''INSERT INTO VOCABULARY
                                (word, phonetics, pos, translation, example_sentence, example_translation, description, related_image)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            c.execute(sql_insert_new_word, tuple(sql_insert_word_values))
            conn.commit()
            log.debug("MODEL: Inserted New Word in DB.")
        except:
            log.error("MODEL: Inserting Word failed")

        self.load_db()
    

    def import_words_db(self, import_dict):
        
        sql_import_word = '''INSERT INTO VOCABULARY VALUES (?,?,?,?,?,?,?)'''
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        word_values = []
        
        for imp_word in import_dict:
            temp_list = []
            
            for key, value in imp_word.items():
                temp_list.append(value)
            word_values.append(tuple(temp_list))
        try:
            c.executemany(sql_import_word, word_values)
            conn.commit()
            log.debug("MODEL: Imported Word from File")
        except:
            log.error("MODEL: Importing Word from File failed")
         
        self.load_db()

    
    def delete_word(self, word_id):
        print(word_id)
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
    
    

    def populate_database(self, population_words=()):
        sql_populate_db = '''INSERT INTO VOCABULARY (word, phonetics, pos, translation, example_sentence, example_translation, description) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        c = conn.cursor()

        try:
            c.execute(sql_populate_db, population_words)
            conn.commit()
            log.debug("MODEL: Successfully populated Database.")
        except:
            log.error("MODEL: Failed populating Database.")

        


class word():
    def __init__(self, **kwargs):
        self.attributes = {}
        for key, value in kwargs.items():
            self.attributes[key] = value
    




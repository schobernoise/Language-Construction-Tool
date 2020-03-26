from controllers import utils
from models import word
import sqlite3

class voc_model():
    def __init__(self):
        pass

    def load_db(self, db_file, mode="load"):

        conn = sqlite3.connect(db_file)

        if mode == "create":
            sql_create_voc = '''CREATE TABLE VOCABULARY
                                ([generated_id] INTEGER PRIMARY KEY,
                                [word] TEXT,
                                [translation] TEXT,
                                [pos] TEXT,
                                [example_sentence] TEXT,
                                [example_translation] TEXT,
                                [description] TEXT,
                                [related_words] TEXT,
                                [related_image] BLOB)'''
            
            sql_create_pos = 
            c = conn.cursor()
            c.execute(sql_create_voc)

            
        elif mode =="load":
            pass




class word()
    def __init__(self):
        pass
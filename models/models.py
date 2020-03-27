from controllers import utils
from models import word
import sqlite3
from PIL import Image
import io

class voc_model():
    def __init__(self):
        pass

    def load_db(self, db_file, mode="load"):

        conn = sqlite3.connect(db_file)
        self.vocabulary = []

        if mode == "create":
            sql_create_voc = '''CREATE TABLE VOCABULARY
                                ([word_id] INTEGER PRIMARY KEY,
                                [word] varchar(255),
                                [translation] TEXT,
                                [pos] varchar(255),
                                [example_sentence] TEXT,
                                [example_translation] TEXT,
                                [description] TEXT,
                                [related_words] TEXT,
                                [related_image] BLOB)'''
            

            c = conn.cursor()
            c.execute(sql_create_voc)

            
        elif mode =="load":
            sql_load_voc = "SELECT * FROM VOCABULARY"
            c = conn.cursor()
            c.execute(sql_load_voc)

            rows = c.fetchall()

            for row in rows:
                self.vocabulary.append(word(
                    word_id = row[0],
                    word = row[1],
                    translation = row[2],
                    pos = row[3],
                    example_sentence = row[4],
                    example_translation = row[5],
                    description = row[6],
                    related_words = row[7],
                    related_image = Image.open(io.BytesIO(row[8])) 
                ))

        
    
    def create_word(self, editor_entries):
        pass


class word():
    def __init__(self, **kwargs):
        self.attributes = {}
        for key, value in kwargs.items():
            self.attributes[key] = value
        



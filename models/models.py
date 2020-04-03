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
                                [translation] TEXT NOT NULL,
                                [pos] varchar(255) NOT NULL,
                                [example_sentence] TEXT NOT NULL,
                                [example_translation] TEXT NOT NULL,
                                [description] TEXT NOT NULL,
                                [related_words] varchar(255) NOT NULL,
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
                    translation = row[2],
                    pos = row[3],
                    example_sentence = row[4],
                    example_translation = row[5],
                    description = row[6],
                    related_words = row[7],
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

        rel_word_ids= []
        for word_name in form_contents[6]:
            if word_name != "Empty Vocabulary":
                for word_object in self.vocabulary:
                    if word_object.attributes["word"] == word_name:
                        rel_word_ids.append(word_object.attributes["word_id"])

        for i, value in enumerate(form_contents):
            if i != 6:
                sql_insert_word_values.append(value)
            else:
                if rel_word_ids != []:
                    sql_insert_word_values.append(str(rel_word_ids))
                else:
                    sql_insert_word_values.append("")

        sql_insert_new_word = '''INSERT INTO VOCABULARY
                                (word, pos, translation, example_sentence, example_translation, description, related_words, related_image)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        # print(sql_insert_word_values[5], sql_insert_word_values[6])

        try:
            c.execute(sql_insert_new_word, tuple(sql_insert_word_values))
            conn.commit()
            log.debug("MODEL: Inserted New Word in DB.")
        except:
            log.error("MODEL: Inserting Word failed")
         
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



class word():
    def __init__(self, **kwargs):
        self.attributes = {}
        for key, value in kwargs.items():
            self.attributes[key] = value
    

    def callback(self, event=None):
        print(self.attributes["word"])



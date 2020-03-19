from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel
from controllers import utils
from controllers import log

import sqlite3
from sqlite3 import Error

class lct_voc(QObject):

    WORD, POS = range(2)

    def __init__(self):
        super().__init__()
        self.qt_vocab = self.create_vocab_model(self)
    

    def load_db(self, db_file, mode):
        sql_create_vocabulary = '''CREATE TABLE VOCABULARY
                                ([generated_id] INTEGER PRIMARY KEY,
                                [word] TEXT NOT NULL,
                                [translation] TEXT NOT NULL,
                                [pos] TEXT NOT NULL,
                                [example_sentence] TEXT NOT NULL,
                                [example_translation] TEXT NOT NULL,
                                [description] TEXT NOT NULL,
                                [related_words] TEXT NOT NULL,
                                [related_image] BLOB NOT NULL)'''

        ######## CONNECT DB FILE

        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            # log.debug(f"MODEL: Successfully created {}".format(db_file))
            log.debug("MODEL: Successfully created")
        except:
            return False
            log.error("Couldn't create Database File")
        
        ######### CREATE AND LOAD TABLES

        if mode == "create":
            try:
                c.execute(sql_create_vocabulary)
                log.debug("MODEL: Successfully Created new Tables")
                return []
            except:
                log.error("MODEL: Couldn't create Tables")
                pass
        elif mode == "load":
            try:
                c.execute('SELECT * FROM vocabulary')
                data = c.fetchall()
                log.debug("MODEL: Successfully loaded Data from DB.")
                print(data)
            except:
                data = []
                log.error("MODEL: Couldn't Fetch All.")
            finally:
                self.add_vocab_model(self.qt_vocab, data)
                return data


    def convertToBinaryData(self, image_name):
        #Convert digital data to binary format
        with open(image_name, 'rb') as file:
            blobData = file.read()
        return blobData

    
    
    def write_word_to_db(self, word_data):
        pass
    
    def load_word_from_db(self, id):
        pass

    def create_vocab_model(self,parent):
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.WORD, Qt.Horizontal, "word")
        model.setHeaderData(self.POS, Qt.Horizontal, "pos")
        return model

    def add_vocab_model(self, model, word_data):
        model.insertRow(0)
        model.setData(model.index(0, self.WORD), word_data[1])
        model.setData(model.index(0, self.POS), word_data[3])
 

    
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from controllers import utils
from controllers import log


class lct_voc(QSqlRelationalTableModel):

    def __init__(self, db_file, mode):
        super().__init__()
        
        if mode == "create":
            self.create_db(db_file)
        elif mode == "load":
            self.load_db(db_file)
        
        # self.initializeModel()

        # self.vocabulary = self.load_db(db_file. mode)

    def initializeModel(self):
        self.setTable('VOCABULARY')
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.select()
        self.setHeaderData(0, Qt.Horizontal, "id")
        self.setHeaderData(1, Qt.Horizontal, "word")
        self.setHeaderData(2, Qt.Horizontal, "translation")
        self.setHeaderData(2, Qt.Horizontal, "pos")
        self.setHeaderData(2, Qt.Horizontal, "example_sentence")
        self.setHeaderData(2, Qt.Horizontal, "example_translation")
        self.setHeaderData(2, Qt.Horizontal, "related_words")
        self.setHeaderData(2, Qt.Horizontal, "related_image")
    
    def create_db(self, db_file):

        sql_create_vocab = '''CREATE TABLE VOCABULARY
                            ([generated_id] INTEGER PRIMARY KEY,
                            [word] TEXT NOT NULL,
                            [translation] TEXT NOT NULL,
                            [pos] TEXT NOT NULL,
                            [example_sentence] TEXT NOT NULL,
                            [example_translation] TEXT NOT NULL,
                            [description] TEXT NOT NULL,
                            [related_words] TEXT NOT NULL,
                            [related_image] BLOB NOT NULL)'''

        sql_create_rel_words = '''CREATE TABLE RELATED
                                ([])'''

        print(db_file)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_file)  
         
        query = QSqlQuery(db)
        query.prepare(sql_create_vocab)    
        query.exec()
        self.setQuery(query)

        return True


    def load_db(self, db_file):

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_file)

        if self.db.open():
            log.debug('MODEL: connect to SQL Server successfully')
            # return True
        else:
            log.error('MODEL: connection failed')
            # return False

        qry = QSqlQuery(self.db)
        log.info('MODEL: Processing Query')
        qry.prepare('SELECT * FROM VOCABULARY')
        qry.exec()
        query = QSqlQuery(db_file)
        self.setQuery(qry)



    def convertToBinaryData(self, image_name):
        #Convert digital data to binary format
        try:
            with open(image_name, 'rb') as file:
                blobData = file.read()
            log.debug("MODEL: Successfully reading Image")
            return blobData
        except:
            log.error("MODEL: Reading Image failed")    
            pass


    def save_image(self, image_file):
        self.setData(self.index(0, 7), "XXXX")
        self.submitAll()

        # self.convertToBinaryData(image_file)
    
    def write_word_to_db(self, word_data):
        pass
    
    def load_word_from_db(self, id):
        pass


    
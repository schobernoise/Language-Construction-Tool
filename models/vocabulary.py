from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from controllers import utils
from controllers import log


class lct_voc(QSqlTableModel):

    def __init__(self, db_file, mode):
        super().__init__()
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        print(db_file)
        self.db.setDatabaseName(db_file)
        self.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.setTable("VOCABULARY") 
        self.select()

        print(self.rowCount())
   


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
        print("BEFORE " + self.record(0).value("related_words"))
        try:
            self.setData(self.index(0, 7), "XXXXX")
            self.submitAll()
            print("SUCCESS")
        except:
            print("FAIL")
        
        print("AFTER " + self.record(0).value("related_words"))
        
        # self.convertToBinaryData(image_file)
    
    def write_word_to_db(self, word_data):
        pass
    
    def load_word_from_db(self, id):
        pass


    
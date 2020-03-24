from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from controllers import utils
from controllers import log


class vocab_model(QSqlTableModel):

    def __init__(self, db_file, mode):

        # If any, close old connections
        
        # The Database File has to be linked before the Super Class is called
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_file)
        # print(dir(QSqlTableModel))
        self.db_file = db_file

        # Then the QSqlTableModel gets initialized, so we can use all its methods
        super().__init__()

        # It automatically creates a new file, if it is in create mode
        if mode == "create":
            query = QSqlQuery(self.db)
            query.exec_('''CREATE TABLE VOCABULARY
                            ([generated_id] INTEGER PRIMARY KEY,
                            [word] TEXT,
                            [translation] TEXT,
                            [pos] TEXT,
                            [example_sentence] TEXT,
                            [example_translation] TEXT,
                            [description] TEXT,
                            [related_words] TEXT,
                            [related_image] BLOB)''')

        self.setEditStrategy(QSqlRelationalTableModel.OnRowChange)
        self.setTable("VOCABULARY") 
        self.select()

    

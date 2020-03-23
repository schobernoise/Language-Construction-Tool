from PyQt5.QtCore import QObject, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import QMainWindow, QDataWidgetMapper, QTreeView
from PyQt5.QtGui import *

from controllers import utils
from controllers import log
from models.vocabulary import vocab_model
from views.new_vocab import new_vocab
from views.word_editor import word_editor

class lct_controller(QObject):
    def __init__(self, main_win, start_up):
        super().__init__()
        log.info("WELCOME TO THE LANGUAGE CONSTRUCTION TOOL")
        log.info("#########################################")
        
        self.main_win = main_win
        self.start_up = start_up
        self.connect_signals()
        self.load_interface()
        # self.insert_word_data()


    def load_interface(self, db_file="", name=""):
        print("LOADING INTERFACE " + name)
        if db_file != "" and name == "":
            self.vocab = vocab_model(db_file, "load")
        elif name != "" and db_file == "":
            db_file = "data/" + name + ".db"
            self.vocab = vocab_model(db_file, "create")
        else:
            self.vocab = vocab_model("data/start.db", "load")
            self.start_up = False
        
        self.main_win.vocab_tv.setModel(self.vocab)
        for i in range(9):
            if i != 1:
                self.main_win.vocab_tv.hideColumn(i)
        self.main_win.vocab_tv.header().hide()
        


    def connect_signals(self):
        self.main_win.new_vocab.clicked.connect(self.show_new_voc)
        self.main_win.add_word.clicked.connect(self.show_word_editor)
        # print(dir(QModelIndex))
        self.main_win.vocab_tv.clicked.connect(self.insert_word_data)
        

    def insert_word_data(self):
        index = self.main_win.vocab_tv.selectedIndexes()
        record = self.vocab.record(index[0].internalId())

        self.main_win.word_label.setText(record.value(1))
        self.main_win.translation_label.setText(record.value(2))
        self.main_win.pos_label.setText(record.value(3))
        self.main_win.example_sentence.setText(record.value(4))
        self.main_win.example_sentence_2.setText(record.value(5))
        self.main_win.description.setText(record.value(6))

        qimg = QImage.fromData(record.value(8))
        qimg = qimg.scaledToWidth(800)
        self.main_win.word_image.setPixmap(QPixmap(qimg))
        
    def show_new_voc(self):
        self.dialog = new_vocab()
        voc_name = self.dialog.lineEdit.text()
        self.dialog.buttonBox.accepted.connect(lambda x=voc_name:self.load_interface(name=x))
        self.dialog.exec_()
        # if self.dialog.lineEdit.text() != "":
        
        print("NAME IS " + voc_name)
        
    

    def save_data_to_model(self):
        pass
    
    
    def show_word_editor(self):
        self.dialog = word_editor()
        self.dialog.exec_()

        
        

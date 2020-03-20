from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from controllers import utils
from controllers import log
from models.vocabulary import lct_voc

class lct_controller(QObject):
    def __init__(self, main_win, start_up):
        super().__init__()
        log.info("WELCOME TO THE LANGUAGE CONSTRUCTION TOOL")
        log.info("#########################################")
        
        self.main_win = main_win
        self.util = utils
        self.start_up = start_up
        
        if self.start_up == True:
            self.start_mode()
  
    def start_mode(self):
        self.vocab = lct_voc()
        self.vocabulary = self.vocab.load_db("data/start.db", "load")
        self.connect_models()
        self.connect_buttons()

    def loaded_mode(self, db_file="", name=""):
        if db_file != "":
            self.vocab = lct_voc()
            self.vocabulary = self.vocab.load_db(db_file, "load")
        elif name != "":
            db_file = "data/" + name + ".db"
            self.vocab = lct_voc()
            self.vocabulary = self.vocab.load_db(db_file, "create")
        
        
        print(self.vocabulary)
        


    def display_data(self):
        pass
    
    def connect_models(self):
        self.main_win._ui.vocab_tv.setModel(self.vocab.qt_vocab)
    
    def connect_buttons(self):
        self.main_win._ui.new_vocab.clicked.connect(lambda:self.loaded_mode(name="test"))



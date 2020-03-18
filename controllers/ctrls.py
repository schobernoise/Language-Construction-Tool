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



    def loaded_mode(self, db_file="", name=""):
        if db_file != "":
            self.vocab = lct_voc()
            self.vocabulary = self.vocab.load_db(db_file, "load")
        elif name != "":
            db_file = name + ".db"
            self.vocab = lct_voc()
            self.vocabulary = self.vocab.load_db(db_file, "create")
        
        # print(self.vocabulary)
        
        # self.load_voc_into_list(self.vocabulary)

    
    def load_voc_into_list(self, voc):
        pass
    



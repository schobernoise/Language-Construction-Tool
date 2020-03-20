from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDataWidgetMapper

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
        self.start_vocab = lct_voc("data/start.db", "load")
        self.main_win.vocab_tv.setModel(self.start_vocab)
        # for i in range(9):
        #     if i != 1:
        #         self.main_win.vocab_tv.hideColumn(i)
        self.main_win.vocab_tv.header().hide()

        self.connect_buttons()

    def loaded_mode(self, db_file="", name=""):
        if db_file != "":
            self.vocab = lct_voc(db_file, "load")
        elif name != "":
            db_file = "data/" + name + ".db"
            self.vocab = lct_voc(db_file, "create")

    def connect_buttons(self):
        self.main_win.new_vocab.clicked.connect(lambda:self.start_vocab.save_image("ressources/word_image.jpg"))



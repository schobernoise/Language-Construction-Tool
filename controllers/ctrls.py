from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDataWidgetMapper

from controllers import utils
from controllers import log
from models.vocabulary import vocab_model

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
            crawler = self.main_win.vocab_tv.selectedIndexes()[0].model().item(self.main_win.vocab_tv.selectedIndexes()[0].row())
            print(crawler.uri)
  
    def start_mode(self):
        self.start_vocab = vocab_model("data/start2.db", "create")
        self.main_win.vocab_tv.setModel(self.start_vocab)
        for i in range(9):
            if i != 1:
                self.main_win.vocab_tv.hideColumn(i)
        self.main_win.vocab_tv.header().hide()

        self.connect_buttons()

    def loaded_mode(self, db_file="", name=""):
        if db_file != "":
            self.vocab = vocab_model(db_file, "load")
        elif name != "":
            db_file = "data/" + name + ".db"
            self.vocab = vocab_model(db_file, "create")

    def connect_buttons(self):
        # self.main_win.new_vocab.clicked.connect(lambda:self.start_vocab.save_image("ressources/word_image.jpg"))
        pass

    def insert_word_data(self, item):
        self.main_win.vocab_tv.
        self.main_win.description.setText(_translate("MainWindow", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."))
        self.main_win.translation_label.setText(_translate("MainWindow", "Translation"))
        self.main_win.example_sentence.setText(_translate("MainWindow", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."))
        self.main_win.rel_header.setText(_translate("MainWindow", "Related Words"))
        self.main_win.example_sentence_2.setText(_translate("MainWindow", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."))
        self.main_win.pos_label.setText(_translate("MainWindow", "Verb"))
        self.main_win.description_header.setText(_translate("MainWindow", "Description"))
        self.main_win.word_label.setText(_translate("MainWindow", "Word Item"))

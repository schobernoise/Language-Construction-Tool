import tkinter as tk
from tkinter import ttk

from controllers import utils
from models.models import voc_model
from views.main_views import main_frame


class lct_controller():
    def __init__(self, root, start_up):
        self.vocab = voc_model()
        self.main_win = main_frame(root)
        self.main_win.withdraw() 

        self.start_up = start_up

        if self.start_up == True:
            self.load_vocabulary()
            self.start_up = False
    
    def load_vocabulary(self, name="", db_file="")
        self.vocab = voc_model()

        if name != "" and db_file = "":
            db_file = "data/" + name + ".db"
            self.vocab.load_db(db_file, mode="create")
        elif name = "" and db_file != "":
            self.vocab.load_db(db_file, mode="load")
        else:
            db_file="data/start.db"
            self.vocab.load_db(db_file, mode="load")

        
        


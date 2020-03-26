import tkinter as tk
from tkinter import ttk

from controllers import utils
from models.models import voc_model
from views.main_views import main_frame


class lct_controller():
    def __init__(self, root, start_up):
        self.vocab = voc_model()
        self.main_win = main_frame(root)
        self.start_up = start_up

        self.main_win.withdraw() 
        


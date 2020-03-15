import tkinter as tk
from tkinter import ttk

from controllers.utils import utils
from models.models import lct_voc
from views.views import main_frame


class lct_controller():
    def __init__(self, root, start_up):
        self.vocab = lct_voc()
        self.main_win = main_frame(root)
        self.util = utils
        self.start_up = start_up

        self.main_win.withdraw() 
        


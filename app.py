import tkinter as tk
import os
from pathlib import Path
from controllers import log
import logging

from controllers.ctrls import lct_controller
from views.views import main_frame
from models.models import lct_voc


if __name__ == '__main__':
    print(dir(log))
    log.info("WELCOME TO THE LANGUAGE CONSTRUCTION TOOL")
    root = tk.Tk()  # TKINTER OBJECT
    app = lct_controller(root,  start_up=True) # GUI CONTROLLER

    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

    root.mainloop() # START WINDOW


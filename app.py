import tkinter as tk
import os
from pathlib import Path
import logging

from controllers import log
from controllers import utils
from controllers.ctrls import lct_controller


if __name__ == '__main__':
    log.info("#########################################")
    log.info("WELCOME TO THE LANGUAGE CONSTRUCTION TOOL")
    root = tk.Tk()  # TKINTER OBJECT
    conf = utils.Config()
    app = lct_controller(root, conf) # GUI CONTROLLER

    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

    root.mainloop() # START WINDOW
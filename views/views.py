import tkinter as tk
from tkinter import ttk

class common_win:
    def __init__(self):
        pass

    def _quit(self):
        pass

class main_frame(common_win, tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        super().__init__()
        self.main_win = master 
        self.protocol('WM_DELETE_WINDOW', self.main_win.destroy)

        self.build_geruest()

    
    def build_geruest(self):
        for i in range(10):
            tk.Button(self.main_win, text=i).pack(fill="both", expand=1)
      
    
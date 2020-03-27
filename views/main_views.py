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

        ######### GUI INFO SETUP ##################

        self.main_win.geometry("1024x768")     
        self.main_win.minsize(1024, 768)
        self.main_win.title("Discodos")

        ##########################################

        self.build_geruest()

    
    def build_geruest(self):
        
        # #########################################
        # CREATE TABS
        # ##########################################

        self.tab_control = ttk.Notebook(self.main_win)            
        self.voc_tab = ttk.Frame(self.tab_control)                     
        self.tab_control.add(self.voc_tab, text="Vocabulary")          
        self.con_tab = ttk.Frame(self.tab_control)                     
        self.tab_control.add(self.con_tab, text='Construction')      
        self.tab_control.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")  

        ################### 12 GRID SYSTEM ######################
        
        for i in range(12):
            self.main_win.columnconfigure(i, weight = 1)
            self.main_win.rowconfigure(i, weight = 1)
            self.voc_tab.columnconfigure(i, weight = 1)
            self.voc_tab.rowconfigure(i, weight = 1)
            

        self.word_list = ttk.Treeview(self.voc_tab, show="tree")
        self.word_list.grid(column=0, row=0, columnspan=4, rowspan=12, sticky="wns")    
        

        self.word_header = tk.Label(self.main_win, text="Word Header", font=("Consolas", 24))
        self.word_header.grid(column=4, row=1, sticky="nw")
        self.word_header.bind("<Button-1>", self.insert_edit)
        

        self.editor = tk.Entry(self.main_win)
        self.editor.grid(column=4, row=10, sticky="sw")

    
    def insert_edit(self, event):
        self.editor.delete(0, tk.END)
        self.editor.insert(0,self.word_header["text"])
        print("TEST")


        


      
    
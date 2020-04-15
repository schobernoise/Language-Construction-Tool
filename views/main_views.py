import tkinter as tk
from tkinter import ttk
from tk_html_widgets import HTMLLabel

from functools import partial

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
        self.main_win.title("Language Construction Tool")

        ###########  BUILD GUI ##################

        self.build_geruest()

    
    def build_geruest(self):

        # BUILD MENU
        self.menu = tk.Menu(self.main_win)
        self.main_win.configure(menu=self.menu)
        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.vocmenu = tk.Menu(self.menu, tearoff=0)
        self.conmenu = tk.Menu(self.menu, tearoff=0)
        
        # #########################################
        # CREATE TABS
        # ##########################################

        self.tab_control = ttk.Notebook(self.main_win)            
        self.voc_tab = ttk.Frame(self.tab_control)                     
        self.tab_control.add(self.voc_tab, text="Vocabulary")          
        self.con_tab = ttk.Frame(self.tab_control)                     
        self.tab_control.add(self.con_tab, text='Construction')      
        self.tab_control.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")  

        s = ttk.Style()
        s.configure('TNotebook', tabposition='ne') #'ne' as in compass direction
        
        ################### 12 GRID SYSTEM ######################
        
        for i in range(12):
            self.main_win.columnconfigure(i, weight = 1)
            self.main_win.rowconfigure(i, weight = 1)
            self.voc_tab.columnconfigure(i, weight = 1)
            self.voc_tab.rowconfigure(i, weight = 1)

        ################# TREE VIEW ############################

        column_width=100

        self.word_list = ttk.Treeview(self.voc_tab)
        self.word_list.grid(column=0, row=0,  rowspan=11, columnspan=4, sticky="wnse") 
        self.word_list["columns"]=("translation")
        self.word_list.column("translation", width=column_width)
        self.word_list.column("#0", width=column_width)

        self.word_list.heading("#0",text="Transliteration")
        self.word_list.heading("translation",text="Translation")

        ###### COLOR BUG FIX ###########
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground'),
        background=self.fixed_map('background'))

        
        #############################################################
        ######################## WORD FRAME #########################
        #############################################################

        self.word_frame = tk.Frame(self.voc_tab)
        self.word_info_frame = tk.LabelFrame(self.word_frame, text="Word Info")
        self.examples_frame = tk.LabelFrame(self.word_frame, text="Examples")
        self.description_frame = tk.LabelFrame(self.word_frame, text="Description")

        ############ WEIGHTS ########################

        for i in range(10):
            self.word_frame.rowconfigure(i, weight=1)
            self.word_frame.columnconfigure(i, weight=1)

            self.word_info_frame.rowconfigure(i, weight=1)
            self.word_info_frame.columnconfigure(i, weight=1)

            self.examples_frame.rowconfigure(i, weight=1)
            self.examples_frame.columnconfigure(i, weight=1)

            self.description_frame.rowconfigure(i, weight=1)
            self.description_frame.columnconfigure(i, weight=1)

        ########## WORD HEADER ################

        self.word_header = tk.Label(self.word_frame, text="placeholder", font=("Consolas", 36,"bold"))
        self.word_header.grid(column=1, row=0, sticky="ne")

            ############### WORD INFO FRAME ###############
            ###############################################
        
        ############ PHONETICS ######################

        tk.Label(self.word_info_frame, text="Phonetics", font=("Consolas", 10,"bold")).grid(column=0, row=0, sticky="nw", padx=5, pady=5)
        self.phonetics_label = tk.Label(self.word_info_frame, text="placeholder")
        self.phonetics_label.grid(column=1, row=0, sticky="nw")

        ########### PART OF SPEECH ###################

        tk.Label(self.word_info_frame, text="Part of Speech", font=("Consolas", 10,"bold")).grid(column=0, row=1, sticky="nw", padx=5, pady=5)
        self.pos_label = tk.Label(self.word_info_frame, text="placeholder")
        self.pos_label.grid(column=1, row=1, sticky="nw")

        ########### TRANSLATION ###################

        tk.Label(self.word_info_frame, text="Translation", font=("Consolas", 10,"bold")).grid(column=0, row=2, sticky="nw", padx=5, pady=5)
        self.translation_label = tk.Label(self.word_info_frame, text="placeholder")
        self.translation_label.grid(column=1, row=2, sticky="nw")


            ############### EXAMPLE FRAME ###############
            ###############################################
        
        ########### EXAMPLE SENTENCE ###################

        tk.Label(self.examples_frame, text="Example Sentence", font=("Consolas", 10,"bold")).grid(column=0, row=0, sticky="nw", padx=5, pady=5)
        self.example_label = tk.Label(self.examples_frame, text="This is a placeholder sentence.")
        self.example_label.grid(column=1, row=1, sticky="nw")

        ttk.Separator(self.examples_frame, orient="horizontal").grid(row=2, column=0, columnspan=10, sticky="nesw")

        ########### EXAMPLE TRANSLATION ###################

        tk.Label(self.examples_frame, text="Example Translation", font=("Consolas", 10,"bold")).grid(column=0, row=3, sticky="nw", padx=5, pady=5)
        self.example_translation_label = tk.Label(self.examples_frame, text="This is a placeholder sentence")
        self.example_translation_label.grid(column=1, row=4, sticky="nw")

            ############### DESCRIPTION FRAME ###############
            ###############################################

        ########### DESCRIPTION ##########################

        self.description = HTMLLabel(self.description_frame, html="", width=40, height=10, font=("Times New Roman", 16), padx=40)
        self.description.grid(column=0, row=0, sticky="nsew")


            ################## BUTTON FRAME #########################
            ########################################################

        self.button_frame = ttk.Frame(self.voc_tab)

        voc_button_labels = ["add", "delete"]
        self.voc_buttons = []

        for label in voc_button_labels:
            self.voc_buttons.append(tk.Button(self.button_frame, text=label))

        h=0
        for i, button in enumerate(self.voc_buttons):
            button.grid(column=h, row=0, sticky="nsew", columnspan=2)
            h = h+2
        
        self.button_frame.grid(column=0, row=11, rowspan=4, columnspan=4, sticky="nsew")
        for i in range(4):
            self.button_frame.rowconfigure(i, weight=1)
            self.button_frame.columnconfigure(i, weight=1)


        ############# FRAME GRID #######################

        self.word_info_frame.grid(column=1, row=2, sticky="nsew")
        self.examples_frame.grid(column=1, row=5, sticky="nsew")
        self.description_frame.grid(column=1, row=7, sticky="nsew")
        self.word_frame.grid(column=6, row=1, columnspan=5, rowspan=10, sticky="nsew")

            ############## SIDE BAR ###########################
            ##################################################
        

        ################## RELATED IMAGE ######################

        ttk.Separator(self.voc_tab, orient="vertical").grid(row=0, column=11, rowspan=12, sticky="nesw")

        self.related_image = tk.Canvas(self.voc_tab, width=200, height=200)
        self.related_image.grid(column=12, row=1, sticky="nesw")


        ################ VOC INFO FRAME ##########################

        self.voc_info_frame = tk.LabelFrame(self.main_win, text="Vocabulary Info")
        self.voc_info_frame.grid(column=11, row=8, sticky="nsew", padx=5, pady=5)

        tk.Label(self.voc_info_frame, text="Vocabulary Name", font=("Consolas", 10,"bold")).grid(column=0, row=0, sticky="nw", padx=5, pady=5)
        self.voc_name_label = tk.Label(self.voc_info_frame, text="placeholder")
        self.voc_name_label.grid(column=0, row=1, sticky="nw")

        tk.Label(self.voc_info_frame, text="Author", font=("Consolas", 10,"bold")).grid(column=0, row=2, sticky="nw", padx=5, pady=5)
        self.author_label = tk.Label(self.voc_info_frame, text="placeholder")
        self.author_label.grid(column=0, row=3, sticky="nw")

        tk.Label(self.voc_info_frame, text="Translation Language", font=("Consolas", 10,"bold")).grid(column=0, row=4, sticky="nw", padx=5, pady=5)
        self.trans_lang_label = tk.Label(self.voc_info_frame, text="placeholder")
        self.trans_lang_label.grid(column=0, row=5, sticky="nw")

        tk.Label(self.voc_info_frame, text="Word Count", font=("Consolas", 10,"bold")).grid(column=0, row=6, sticky="nw", padx=5, pady=5)
        self.word_count = tk.Label(self.voc_info_frame, text="4356")
        self.word_count.grid(column=0, row=7, sticky="nw")

        tk.Label(self.voc_info_frame, text="Description", font=("Consolas", 10,"bold")).grid(column=0, row=8, sticky="nw", padx=5, pady=5)
        self.voc_description = tk.Label(self.voc_info_frame, text=" This is a placeholder Sentence.")
        self.voc_description.grid(column=0, row=9, sticky="nw")


        ######### STATUS BAR #######################

        self.status=tk.StringVar()  
        self.status_bar = tk.Label(self.main_win, textvariable=self.status, anchor=tk.W, bd=1, relief=tk.SUNKEN)
        self.status_bar.grid(row=12, column=0, columnspan=12, rowspan=1, sticky="nwes")
        self.status.set("Ready...")
    

    def fixed_map(self, option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option) if
        elm[:2] != ('!disabled', '!selected')]
    

class new_vocabulary_form():
    def __init__(self):
        self.new_vocab_win = tk.Toplevel()
        self.new_vocab_win.geometry("280x200")
        self.new_vocab_win.title("New Vocabulary")
        self.new_vocab_win.resizable(0,0)
        self.new_vocab_win.attributes('-topmost', True)
        self.create_widgets()
    

    def create_widgets(self):
        self.entries = {
            "name" : ["Vocabulary Name"],
            "author" : ["Author"],
            "language" : ["Translation Language"],
            "notes": ["Vocabulary Notes"]
                        }
        row = 0
        for name, entry in self.entries.items():
            entry.append(tk.Label(self.new_vocab_win, text=entry[0], padx=10, pady=10))
            entry.append(tk.Entry(self.new_vocab_win))
            for i, entropy in enumerate(entry):
                if i != 0:
                    entropy.grid(row=row, column=i-1, sticky="nsew")
            row += 1
        
        self.submit_button = tk.Button(self.new_vocab_win, text="Create Vocabulary")
        self.submit_button.grid(row=len(self.entries), padx=10, pady=10, column=0, columnspan=2, sticky="nsew")

        

class new_word_form():
    def __init__(self, pos_list):
        self.pos_list = pos_list
        self.new_word_win = tk.Toplevel()
        self.new_word_win.geometry("800x520")
        self.new_word_win.title("Create New Word")
        self.new_word_win.resizable(0,0)
        self.new_word_win.attributes('-topmost', True)

        self.create_widgets()


    def create_widgets(self):
        self.entries = {
            "word" : ["Word Literal"],
            "phonetics" : ["Phonetics"],
            "pos" : ["Part of Speech"],
            "translation" : ["Translation"],
            "example_sentence": ["Example Sentence"],
            "example_translation" : ["Example Translation"],
            "description" : ["Description"],
            "rel_image" : ["Related Image"]
                        }
        
        for name, entry in self.entries.items():
            entry.append(tk.Label(self.new_word_win, text=entry[0], padx=10, pady=10))
            if name == "description":
                entry.append(tk.Text(self.new_word_win, height=10))
            elif name == "phonetics":
                self.default_pos = tk.StringVar(self.new_word_win)
                self.default_pos.set(self.pos_list[0]) # default value
                entry.append(tk.OptionMenu(self.new_word_win, self.default_pos, *self.pos_list))
            elif name == "rel_image":
                entry.append(tk.Button(self.new_word_win, text="Choose File..."))
            else:
                entry.append(tk.Entry(self.new_word_win))
            
        row = 0
        for name, entry in self.entries.items(): 
            for i, entropy in enumerate(entry):
                if i != 0:
                    entropy.grid(row=row, column=i-1, sticky="nsew")
            row += 1
        
        ############### SUBMIT BUTTON #####################

        self.submit_button = tk.Button(self.new_word_win, text="Add New Word")
        self.submit_button.grid(row=len(self.entries)+3, padx=10, pady=10, column=0, columnspan=2, sticky="nsew")

       

class file_importer():
    def __init__(self):
        self.file_imp_win = tk.Toplevel()
        self.file_imp_win.title("Populate Vocabulary from File")
        # self.file_imp_win.minsize(150, 50) 
        # self.file_imp_win.resizable(0,0)
        self.file_imp_win.attributes('-topmost', True)

        self.file_entry = tk.Entry(self.file_imp_win)
        self.file_entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.file_button = tk.Button(self.file_entry, text="File...")
        self.file_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.submit_button = tk.Button(self.file_imp_win, text="Submit")
        self.submit_button.grid(row=1, column=0, columnspan=2, sticky="nsew")



        



        
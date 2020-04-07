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

        ################# TREE VIEW ############################

        column_width=100

        self.word_list = ttk.Treeview(self.voc_tab, show="tree")
        self.word_list.grid(column=0, row=0,  rowspan=12, sticky="wnse") 
        self.word_list["columns"]=("translation")
        self.word_list.column("translation", width=column_width)
        self.word_list.column("#0", width=column_width)

        ###### COLOR BUG FIX ###########
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground'),
        background=self.fixed_map('background'))

        self.header_frame = tk.Frame(self.voc_tab)

        ######################## GUI DISPLAYS #########################

        self.gui_displays = []  

        ########## WORD HEADER ################
        
        self.word_header = []
        self.word_header.append(tk.Label(self.header_frame, text="", font=("Consolas", 36)))
        self.word_header.append(ttk.Entry(self.header_frame))
        self.word_header.append([0, 0, "nw"])
        self.word_header.append("word")
        self.word_header[0].grid(column=self.word_header[2][0], row=self.word_header[2][1], sticky=self.word_header[2][2])
        self.gui_displays.append(self.word_header)

        ########### PART OF SPEECH ###################

        self.pos_header = []
        self.pos_header.append(tk.Label(self.header_frame, text="", font=("Times New Roman", 24)))
        self.pos_header.append(ttk.Entry(self.header_frame))
        self.pos_header.append([1, 0, "we"])
        self.pos_header.append("pos")
        self.pos_header[0].grid(column=self.pos_header[2][0], row=self.pos_header[2][1], sticky=self.pos_header[2][2])
        self.gui_displays.append(self.pos_header)

        ########### TRANSLATION ###################

        self.translation_header = []
        self.translation_header.append(tk.Label(self.header_frame, text="", font=("Consolas", 12)))
        self.translation_header.append(ttk.Entry(self.header_frame))
        self.translation_header.append([0, 1, "nw"])
        self.translation_header.append("translation")
        self.translation_header[0].grid(column=self.translation_header[2][0], row=self.translation_header[2][1], sticky=self.translation_header[2][2], pady=40)
        self.gui_displays.append(self.translation_header)
        
        ########### EXAMPLE SENTENCE ###################

        self.example_sentence_header = []
        self.example_sentence_header.append(tk.Label(self.header_frame, text="", font=("Consolas", 12)))
        self.example_sentence_header.append(ttk.Entry(self.header_frame))
        self.example_sentence_header.append([0, 2, "nw"])
        self.example_sentence_header.append("example_sentence")
        self.example_sentence_header[0].grid(column=self.example_sentence_header[2][0], row=self.example_sentence_header[2][1], sticky=self.example_sentence_header[2][2])
        self.gui_displays.append(self.example_sentence_header)

        ########### EXAMPLE TRANSLATION ###################

        self.example_translation_header = []
        self.example_translation_header.append(tk.Label(self.header_frame, text="", font=("Consolas", 12)))
        self.example_translation_header.append(ttk.Entry(self.header_frame))
        self.example_translation_header.append([0, 3, "nw"])
        self.example_translation_header.append("example_translation")
        self.example_translation_header[0].grid(column=self.example_translation_header[2][0], row=self.example_translation_header[2][1], sticky=self.example_translation_header[2][2])
        self.gui_displays.append(self.example_translation_header)


        ############# HEADER FRAME GRID #######################

        self.header_frame.grid(column=4, row=1, sticky="nsew", padx=40)

        ########### DESCRIPTION ##########################

        self.description_header = HTMLLabel(self.voc_tab, html="", width=40, height=10, font=("Times New Roman", 16), padx=40)
        self.description_header.grid(column=4, row=4, sticky="nw")

        ################## RELATED IMAGE ######################

        self.related_image  = tk.Canvas(self.voc_tab)
        self.related_image.grid(column=10, row=0, rowspan=12, columnspan=2, sticky="nesw")

        ################ RELATED WORDS ####################

        self.rel_words_frame = tk.Frame(self.voc_tab, padx=20)
        self.rel_words_frame.grid(column=4, row=8, rowspan=3, sticky="nsew")

        self.rel_words_header = tk.Label(self.rel_words_frame, text="Related Words", font=("Consolas", 16))
        self.rel_words_header.grid(column=0, row=0, sticky="nw")

        ################## MENU FRAME #########################

        self.menu_frame = ttk.Frame(self.voc_tab)

        voc_menu_labels = ["add", "delete"]
        self.voc_menu_buttons = []

        self.voc_menu_buttons.append(tk.Menubutton(self.menu_frame, text="File", relief=tk.RAISED))
        for label in voc_menu_labels:
            self.voc_menu_buttons.append(tk.Button(self.menu_frame, text=label))

        # Create pull down menu
        self.voc_menu_buttons[0].menu = tk.Menu(self.voc_menu_buttons[0], tearoff = 0)
        self.voc_menu_buttons[0]["menu"] = self.voc_menu_buttons[0].menu

        for i, button in enumerate(self.voc_menu_buttons):
            button.grid(column=i, row=0, sticky="nsew")
        
        self.menu_frame.grid(column=4, row=0, sticky="nw")
    

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
    def __init__(self, word_list):
        self.new_word_win = tk.Toplevel()
        self.new_word_win.geometry("800x520")
        self.new_word_win.title("Create New Word")
        self.new_word_win.resizable(0,0)
        self.new_word_win.attributes('-topmost', True)
        if word_list != False:
            self.words = word_list
        else:
            self.words = ["Empty Vocabulary"]

        self.create_widgets()


    def create_widgets(self):
        self.entries = {
            "word" : ["Word Literal"],
            "pos" : ["Part of Speech"],
            "translation" : ["Translation"],
            "example_sentence": ["Example Sentence"],
            "example_translation" : ["Example Translation"],
            "description" : ["Description"],
            "rel_words" : ["Related Words"],
            "rel_image" : ["Related Image"]
                        }
        
        for name, entry in self.entries.items():
            entry.append(tk.Label(self.new_word_win, text=entry[0], padx=10, pady=10))
            if name == "description":
                entry.append(tk.Text(self.new_word_win, height=10))
            elif name == "rel_image":
                entry.append(tk.Button(self.new_word_win, text="Choose File..."))
            elif name == "rel_words":
                pass
            else:
                entry.append(tk.Entry(self.new_word_win))
            
            
            
        row = 0
        for name, entry in self.entries.items(): 
            for i, entropy in enumerate(entry):
                if i != 0:
                    entropy.grid(row=row, column=i-1, sticky="nsew")
            row += 1
        
        ################ RELATED WORDS #########################
          
        self.tkvar = tk.StringVar(self.new_word_win)  
            
        tk.Label(self.new_word_win, text="Related Words: ").grid(row=len(self.entries), column=0, sticky=tk.W)

        self.word_to_button = {}
        self.word_variable = tk.StringVar(value="Choose Words...")
        tk.OptionMenu(self.new_word_win, self.word_variable, *self.words).grid(
            row=len(self.entries), column=1, sticky=tk.W
        )

        self.words_frame = tk.Frame(self.new_word_win)
        self.words_frame.grid(row=len(self.entries)+1, column=1, sticky=tk.W)

        self.word_variable.trace(
            "w",
            partial(self.add_related_word, self.word_variable, self.word_to_button, self.words_frame),
        )
        
        ############### SUBMIT BUTTON #####################

        self.submit_button = tk.Button(self.new_word_win, text="Add New Word")
        self.submit_button.grid(row=len(self.entries)+3, padx=10, pady=10, column=0, columnspan=2, sticky="nsew")


    ######### RELATED WORD FUNCTIONS #####################
    
    def add_related_word(self, word_variable, word_to_button, words_frame, *_args):
        word = word_variable.get()
        if word not in word_to_button:
            word_to_button[word] = tk.Button(
                self.words_frame,
                text=word,
                font="Helvetica 7",
                command=partial(
                    self.delete_related_word_button, word_to_button, word
                ),
            )
            self.update_related_word_buttons(word_to_button)


    def delete_related_word_button(self, word_to_button, word):
        word_to_button.pop(word).destroy()
        self.update_related_word_buttons(word_to_button)


    def update_related_word_buttons(self, word_to_button):
        for i, button in enumerate(word_to_button.values()):
            button.grid(column=i, row=0, sticky=tk.NW)
            self.buttons_to_object = word_to_button


class rel_word_editor():
    def __init__(self, word_list, rel_words):
        self.rel_editor_win = tk.Toplevel()
        self.rel_editor_win.title("Edit related words")
        self.rel_editor_win.minsize(150, 50) 
        self.rel_editor_win.resizable(0,0)
        self.rel_editor_win.attributes('-topmost', True)
        
        if word_list != False:
            self.words = word_list
        else:
            self.words = ["Empty Vocabulary"]

        self.tkvar = tk.StringVar(self.rel_editor_win)  
            
        tk.Label(self.rel_editor_win, text="Related Words: ").grid(row=0, column=0, sticky=tk.W)
        
        self.words_frame = tk.Frame(self.rel_editor_win)
        self.words_frame.grid(row=1, column=1, sticky=tk.W)

        self.word_to_button = {}

        for word in rel_words:
            self.word_to_button[word] = tk.Button(
                self.words_frame,
                text=word,
                font="Helvetica 7",
                command=partial(
                    self.delete_related_word_button, self.word_to_button, word
                ),
            )
        self.update_related_word_buttons(self.word_to_button)
        self.word_variable = tk.StringVar(value="Choose Words...")
        tk.OptionMenu(self.rel_editor_win, self.word_variable, *self.words).grid(
            row=0, column=1, sticky=tk.W
        )

        self.word_variable.trace(
            "w",
            partial(self.add_related_word, self.word_variable, self.word_to_button, self.words_frame),
        )

        self.submit_button = tk.Button(self.rel_editor_win, text="Submit")
        self.submit_button.grid(row=2, column=0, sticky="nsew")
    

    def add_related_word(self, word_variable, word_to_button, words_frame, *_args):
        word = word_variable.get()
        if word not in word_to_button:
            word_to_button[word] = tk.Button(
                self.words_frame,
                text=word,
                font="Helvetica 7",
                command=partial(
                    self.delete_related_word_button, word_to_button, word
                ),
            )
            self.update_related_word_buttons(word_to_button)


    def delete_related_word_button(self, word_to_button, word):
        word_to_button.pop(word).destroy()
        self.update_related_word_buttons(word_to_button)


    def update_related_word_buttons(self, word_to_button):
        for i, button in enumerate(word_to_button.values()):
            button.grid(column=i, row=0, sticky=tk.NW)
            self.buttons_to_object = word_to_button



        
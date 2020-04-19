import tkinter as tk
from tkinter import ttk
from tk_html_widgets import HTMLLabel
from controllers import utils

from functools import partial

class common_win:
    def __init__(self):
        pass

    def _quit(self):
        pass

class main_frame(common_win, tk.Toplevel):
    def __init__(self, master, display_data_functions, vocab):
        tk.Toplevel.__init__(self, master)
        super().__init__()
        self.display_data_functions = display_data_functions
        self.vocab = vocab
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

        ################### VOCAB VIEWER ########################

        self.fixed_vocab_viewer = vocab_viewer(self.voc_tab, self.display_data_functions, self.vocab)
        self.fixed_vocab_viewer.grid(column=0, row=0, rowspan=10, columnspan=4, sticky="nsew")

        for i in range(12):
            self.fixed_vocab_viewer.rowconfigure(i, weight=1)
            if i < 4:
                self.fixed_vocab_viewer.columnconfigure(i, weight=1)
        
        ################# CLONE BUTTON ###########################

        self.clone_button = tk.Button(self.voc_tab, text="Clone Vocabulary Viewer")
        self.clone_button.grid(row=11, column=0, rowspan=1, columnspan=4, sticky="nsew")

        
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

        voc_button_labels = ["add", "delete", "edit"]
        self.voc_buttons = []

        for label in voc_button_labels:
            self.voc_buttons.append(tk.Button(self.button_frame, text=label))

        h=0
        for i, button in enumerate(self.voc_buttons):
            button.grid(column=h, row=0, sticky="nsew", columnspan=2)
            h = h+2
        
        self.button_frame.grid(column=0, row=10, rowspan=1, columnspan=4, sticky="nsew")
        for i in range(6):
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

        self.voc_info_frame = tk.LabelFrame(self.voc_tab, text="Vocabulary Info")
        self.voc_info_frame.grid(column=12, row=9, sticky="nsew", padx=5, pady=5)

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
    

class vocab_viewer(tk.Frame):
    def __init__(self, master, display_data_functions, vocab):
        tk.Frame.__init__(self, master)
        self.vocab = vocab
        self.display_data_functions = display_data_functions
        self.create_widgets()
        
    
    def create_widgets(self):

        ################# TREE VIEW ############################

        column_width=100

        self.word_list = ttk.Treeview(self)
        self.word_list.grid(column=0, row=2,  rowspan=10, columnspan=4, sticky="wnse") 
        self.word_list["columns"]=("translation")
        self.word_list.column("translation", width=column_width)
        self.word_list.column("#0", width=column_width)

        self.word_list.heading("#0",text="Transliteration")
        self.word_list.heading("translation",text="Translation")

        ###### COLOR BUG FIX ###########
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground'),
        background=self.fixed_map('background'))

        for i in range(12):
            self.word_list.rowconfigure(i, weight=1)
            if i < 4:
                self.word_list.columnconfigure(i, weight=1)

        ################ UPPER FRAME #####################

        self.upper_frame = tk.Frame(self)
        self.upper_frame.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="nsew")

        for i in range(4):
            self.upper_frame.columnconfigure(i, weight=1)


        ################## SEARCH BAR #############################

        self.search_box = SearchBox(self.upper_frame, command=self.display_vocabulary, placeholder="Search for word", entry_highlightthickness=0)
        self.search_box.grid(column=0, row=0, rowspan=1, columnspan=4, sticky="nsew")
        
        for i in range(4):
            self.search_box.columnconfigure(i, weight=1)
            if i == 1:
                self.search_box.rowconfigure(i, weight=1)
        
        
        ################# POS CHOOSER ###############################

        
        pos_chooser_list = ["all", "unassigned"] + self.vocab.pos_list
        pos_var = tk.StringVar(self)

        self.pos_chooser = tk.Spinbox(self.upper_frame, textvariable=pos_var, values=tuple(pos_chooser_list), command = self.display_vocabulary)
        self.pos_chooser.grid(column=0, row=1, rowspan=1, columnspan=4, sticky="nsew")
        pos_var.set(pos_chooser_list[0])

        for i in range(4):
            self.pos_chooser.columnconfigure(i, weight=1)
            if i == 1:
                self.pos_chooser.rowconfigure(i, weight=1)


    def display_vocabulary(self, text=""):
        self.word_list.delete(*self.word_list.get_children())
        
        for word_object in self.vocab.vocabulary:
            if text in word_object.attributes["transliteration"] or text in word_object.attributes["translation"] or text == "":
                if word_object.attributes["pos"] == self.pos_chooser.get() or self.pos_chooser.get() == "all":
                    self.word_list.insert("", "end", text=word_object.attributes["transliteration"], values=word_object.attributes["translation"], tags=(word_object.attributes["word_id"],))
                    self.word_list.tag_bind(word_object.attributes["word_id"],'<<TreeviewSelect>>', lambda event, wo=word_object: self.display_data_functions[0](event, wo))
                elif self.pos_chooser == "unassigned" and word_object.attributes["pos"] == "-":
                    self.word_list.insert("", "end", text=word_object.attributes["transliteration"], values=word_object.attributes["translation"], tags=(word_object.attributes["word_id"],))
                    self.word_list.tag_bind(word_object.attributes["word_id"],'<<TreeviewSelect>>', lambda event, wo=word_object: self.display_data_functions[0](event, wo))
        try:
            self.focus_object(self.word_list)
        except IndexError:
            self.display_data_functions[1]()
    

    def focus_object(self, tree_view, pos=0):
        child_id = tree_view.get_children()[int(pos)]
        tree_view.focus(child_id)
        tree_view.selection_set(child_id)

    
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
    

    # def command(self, text):
    #     print("search command", "searching:%s"%text)


class edit_vocabulary_form():
    def __init__(self):
        self.edit_vocab_win = tk.Toplevel()
        self.edit_vocab_win.title("New Vocabulary")
        self.edit_vocab_win.resizable(0,0)
        self.edit_vocab_win.attributes('-topmost', True)
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
            entry.append(tk.Label(self.edit_vocab_win, text=entry[0], padx=10, pady=10))
            entry.append(ttk.Entry(self.edit_vocab_win, font=("Calibri 14"), justify='center'))
            for i, entropy in enumerate(entry):
                if i != 0:
                    entropy.grid(row=row, column=i-1, sticky="nsew")
            row += 1
        
        for i in range(4):
            self.edit_vocab_win.columnconfigure(i, weight=1)
        
        self.submit_button = tk.Button(self.edit_vocab_win, text="Submit Vocabulary")
        self.submit_button.grid(row=len(self.entries), padx=10, pady=10, column=0, columnspan=2, sticky="nsew")


class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.contains_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.contains_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.contains_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.contains_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state


class SearchBox(tk.Frame):
    def __init__(self, master, entry_width=30, entry_font=None, entry_background="white", entry_highlightthickness=1, button_text="Search", button_ipadx=10, button_background="#009688", button_foreground="white", button_font=None, opacity=0.8, placeholder=None, placeholder_font=None, placeholder_color="grey", spacing=3, command=None):
        tk.Frame.__init__(self, master)
        
        self._command = command

        self.entry = tk.Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=entry_highlightthickness)
        self.entry.grid(column=0, row=0, columnspan=3, rowspan=1, sticky="nsew")
        
        if entry_font:
            self.entry.configure(font=entry_font)

        if placeholder:
            add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

        self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
        self.entry.bind("<Return>", self._on_execute_command)

        opacity = float(opacity)

        if button_background.startswith("#"):
            r,g,b = utils.hex2rgb(button_background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(button_background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            self._button_activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            self._button_activebackground = '#%04x%04x%04x' % (r,g,b)

        self._button_background = button_background

        self.button_label = tk.Label(self, text=button_text, background=button_background, foreground=button_foreground, font=button_font)
        if entry_font:
            self.button_label.configure(font=button_font)
            
        self.button_label.grid(column=3, row=0, columnspan=1, rowspan=1, sticky="nsew")
        
        self.button_label.bind("<Enter>", self._state_active)
        self.button_label.bind("<Leave>", self._state_normal)

        self.button_label.bind("<ButtonRelease-1>", self._on_execute_command)

    def get_text(self):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            if entry.placeholder_state.contains_placeholder:
                return ""
            else:
                return entry.get()
        else:
            return entry.get()
        
    def set_text(self, text):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            entry.placeholder_state.contains_placeholder = False

        entry.delete(0, "END")
        entry.insert(0, text)
        
    def clear(self):
        self.entry_var.set("")
        
    def focus(self):
        self.entry.focus()

    def _on_execute_command(self, event):
        text = self.get_text()
        self._command(text)

    def _state_normal(self, event):
        self.button_label.configure(background=self._button_background)

    def _state_active(self, event):
        self.button_label.configure(background=self._button_activebackground)


class word_form():
    def __init__(self, pos_list):
        self.pos_list = pos_list
        self.word_win = tk.Toplevel()
        self.word_win.geometry("800x520")
        self.word_win.title("Word Editor")
        self.word_win.resizable(0,0)
        self.word_win.attributes('-topmost', True)

        self.create_widgets()


    def create_widgets(self):
        self.entries = {
            "transliteration" : ["Word Literal"],
            "phonetics" : ["Phonetics"],
            "pos" : ["Part of Speech"],
            "translation" : ["Translation"],
            "example_sentence": ["Example Sentence"],
            "example_translation" : ["Example Translation"],
            "description" : ["Description"],
            "related_image" : ["Related Image"]
                        }
        
        for name, entry in self.entries.items():
            entry.append(tk.Label(self.word_win, text=entry[0], padx=10, pady=10))
            if name == "description":
                entry.append(tk.Text(self.word_win, height=10))
            elif name == "pos":
                self.default_pos = tk.StringVar(self.word_win)
                self.default_pos.set(self.pos_list[0]) # default value
                entry.append(tk.OptionMenu(self.word_win, self.default_pos, *self.pos_list))
            elif name == "related_image":
                entry.append(tk.Button(self.word_win, text="Choose File..."))
            else:
                entry.append(ttk.Entry(self.word_win, justify='center', font=("Calibri 14")))
            
        row = 0
        for name, entry in self.entries.items(): 
            for i, entropy in enumerate(entry):
                if i != 0:
                    entropy.grid(row=row, column=i-1, sticky="nsew")
            row += 1
        
        ############### SUBMIT BUTTON #####################

        self.submit_button = tk.Button(self.word_win, text="Submit Word")
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



        



        
import tkinter as tk
from tkinter import ttk
from tk_html_widgets import HTMLLabel

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
    

class new_vocabulary():
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
        
        tk.Button(self.new_vocab_win, text="Create Vocabulary").grid(row=len(self.entries), padx=10, pady=10, column=0, columnspan=2, sticky="nsew")

        

class new_word():
    def __init__(self):
        self.new_vocab_win = tk.Toplevel()
        self.new_vocab_win.geometry("300x300")
        self.new_vocab_win.title("New Vocabulary")
        self.new_vocab_win.resizable(0,0)
        self.new_vocab_win.attributes('-topmost', True)
    

    def create_widgets(self):
        self.entries = ["word", "translation", "pos", "example_sentence", "example_translation"]
        self.widget_container = []




        
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image
import io
from openpyxl import *

from controllers import utils
from controllers import log
from models.models import voc_model
from views.main_views import *


class lct_controller():
    def __init__(self, root, conf, start_up):
        self.conf = conf
        self.vocab = voc_model()
        self.main_win = main_frame(root)
        self.main_win.withdraw() 
        self.create_voc_menu()
        self.data_handler = data_controller(self.vocab)

        self.pos_list = self.conf.conf["part_of_speech"]

        self.start_up = start_up
        
        if self.start_up == True:
            self.load_vocabulary()
            self.start_up = False
    
    def load_vocabulary(self, name="", db_file="", metadata=[]):
        self.vocab = voc_model()

        if name != "" and metadata != [] and db_file == "":
            self.main_win.status.set("Creating new Vocabulary...")
            db_file = "data/" + utils.string_unify(name) + ".db"
            self.vocab.load_db(db_file=db_file, metadata=metadata, mode="create")
            self.show_tooltips = False
        elif name == "" and metadata == [] and db_file != "":
            self.main_win.status.set("Loading Vocabulary {}".format(db_file))
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = False
        else:
            self.main_win.status.set("Loading Start Vocabulary")
            db_file="data/start.db"
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = True
        
        self.main_win.status.set("Ready...")

        self.display_vocabulary()
        self.main_win.title("Language Construction Tool " + self.vocab.metadata["name"])
        

    def display_vocabulary(self):
        self.main_win.word_list.delete(*self.main_win.word_list.get_children())
        for word_object in self.vocab.vocabulary:
            self.main_win.word_list.insert("", "end", text=word_object.attributes["word"], values=word_object.attributes["translation"], tags=(word_object.attributes["word_id"],))
            self.main_win.word_list.tag_bind(word_object.attributes["word_id"],'<<TreeviewSelect>>', lambda event, wo=word_object: self.display_data(event, wo))
        try:
            self.focus_object(self.main_win.word_list)
        except IndexError:
            self.display_empty_data()
        
    
    def create_voc_menu(self):

        # FILEMENU
        self.main_win.menu.add_cascade(label="File", menu=self.main_win.filemenu)
        self.main_win.filemenu.add_command(label="Create new Vocabulary", command=self.trigger_new_vocabulary)
        self.main_win.filemenu.add_command(label="Open Vocabulary", command=self.trigger_load_vocabulary)
        self.main_win.filemenu.add_separator()
        self.main_win.filemenu.add_command(label="Exit")

        # VOC MENU
        self.main_win.menu.add_cascade(label="Vocabulary", menu=self.main_win.vocmenu)
        self.main_win.vocmenu.add_command(label="Edit Info")
        self.main_win.vocmenu.add_command(label="Import XLS/CSV", command=self.trigger_import)
        self.main_win.vocmenu.add_separator()
        self.main_win.vocmenu.add_command(label="Populate from File...", command=self.trigger_populate_file)
        self.main_win.vocmenu.add_command(label="Populate from Web...")
        

        # CON MENU
        self.main_win.menu.add_cascade(label="Construction", menu=self.main_win.conmenu)
        self.main_win.conmenu.add_command(label="Export Batch...")
        self.main_win.conmenu.add_command(label="Feed File")

        # VOC BUTTONS
        
        self.main_win.voc_buttons[0].configure(command=self.trigger_new_word)
        

    def display_data(self, event, word_object):
        self.main_win.word_header.configure(text=word_object.attributes["word"])
        self.main_win.phonetics_label.configure(text=word_object.attributes["phonetics"])
        self.main_win.pos_label.configure(text=word_object.attributes["pos"])
        self.main_win.translation_label.configure(text=word_object.attributes["translation"])
        self.main_win.example_label.configure(text=word_object.attributes["example_sentence"])
        self.main_win.example_translation_label.configure(text=word_object.attributes["example_translation"])
        self.main_win.description.set_html(html=word_object.attributes["description"])
        img = word_object.attributes["related_image"]
        self.main_win.related_image.image = ImageTk.PhotoImage(img.resize((200, 200), Image.ANTIALIAS))
        self.main_win.related_image.create_image(0, 0, image=self.main_win.related_image.image, anchor='nw')
        self.main_win.related_image.bind('<Double-Button-1>', lambda event, wo=word_object: self.update_related_image(event, wo))
        # DELETE BUTTON
        self.main_win.voc_buttons[1].configure(command=lambda word_id=word_object.attributes["word_id"]:self.trigger_del_word(word_id))
        
        self.display_voc_info()
        # self.main_win.status.set("Ready...")
            
        
    def display_empty_data(self):
        self.main_win.word_header.configure(text="-")
        self.main_win.phonetics_label.configure(text="-")
        self.main_win.pos_label.configure(text="-")
        self.main_win.translation_label.configure(text="-")
        self.main_win.example_label.configure(text="-")
        self.main_win.example_translation_label.configure(text="-")
        self.main_win.description.set_html(html="-")
        img = Image.new('RGB', (500, 1080), color=utils.random_rgb())
   
        self.main_win.related_image.image = ImageTk.PhotoImage(img)     
        self.main_win.related_image.create_image(0, 0, image=self.main_win.related_image.image, anchor='nw')

        self.display_voc_info()


    def display_voc_info(self):
        self.main_win.voc_name_label.configure(text=self.vocab.metadata["name"])
        self.main_win.author_label.configure(text=self.vocab.metadata["author"])
        self.main_win.trans_lang_label.configure(text=self.vocab.metadata["language"])
        self.main_win.word_count.configure(text=str(len(self.vocab.vocabulary)))
        self.main_win.voc_description.configure(text=self.vocab.metadata["notes"])


    def focus_object(self, tree_view, pos=0):
        child_id = tree_view.get_children()[int(pos)]
        tree_view.focus(child_id)
        tree_view.selection_set(child_id)
    

    def edit_description(self, event, word_object):
        self.desc_edit = tk.Toplevel()
        self.desc_edit.geometry("300x300")
        self.desc_edit.title("Edit Description")
        self.desc_edit.resizable(0,0)
        self.desc_edit.attributes('-topmost', True)

        self.desc_text_edit = tk.Text(self.desc_edit, height=15, wrap=tk.WORD)
        self.desc_text_edit.pack()
        self.desc_text_edit.insert(tk.END, word_object.attributes["description"])

        self.desc_edit.bind("<Control-s>", lambda event:self.close_description(event, word_object.attributes["word_id"]))

        tk.Button(self.desc_edit, text="Submit", width=100, command=lambda event:self.close_description(event, word_object.attributes["word_id"])).pack(side="bottom")


    def close_description(self, event, w_id):
        self.vocab.update_word(w_id, 
                                "description", 
                                self.desc_text_edit.get("1.0",tk.END))
        self.desc_edit.destroy()
        self.display_vocabulary()

    
    def update_related_image(self, event, word_object):
        image_filename = utils.open_file_dialog("image")
        if image_filename != "":
            self.vocab.update_word(word_object.attributes["word_id"], "related_image", utils.convertToBinaryData(image_filename))  
            self.display_vocabulary()
        else:
            pass

    
    def trigger_new_vocabulary(self):
        self.new_vocab = new_vocabulary_form()
        self.new_vocab.submit_button.configure(command=self.save_new_vocabulary)


    def save_new_vocabulary(self):
        self.main_win.status.set("Saving new Vocabulary")
        form_contents = []
        for name, entry in self.new_vocab.entries.items():
            form_contents.append(entry[2].get())
        self.load_vocabulary(name=form_contents[0], metadata=form_contents)
        self.new_vocab.new_vocab_win.destroy()
        self.display_vocabulary()
        self.display_empty_data()
    

    def trigger_load_vocabulary(self):
        self.main_win.status.set("Loading Vocabulary...")
        voc_filename = utils.open_file_dialog("database")
        self.load_vocabulary(db_file=voc_filename, metadata=[])
        self.display_vocabulary()
        self.display_empty_data()


    def trigger_new_word(self):
        self.main_win.status.set("Opening New Word Editor")
        self.temp_rel_image = ""
        self.new_word = new_word_form(self.pos_list)
        self.new_word.entries["rel_image"][2].configure(command=self.add_related_image)
        self.new_word.submit_button.configure(command=self.save_new_word)
        

    def add_related_image(self):
        self.temp_rel_image = utils.open_file_dialog("image")
    

    def save_new_word(self):
        self.main_win.status.set("Saving New Word...")
        form_contents = []
        for name, entry in self.new_word.entries.items():
            if name == "rel_image":
                form_contents.append(utils.convertToBinaryData(self.temp_rel_image))
            elif name == "description":
                form_contents.append(entry[2].get("1.0",tk.END))
            else:
                form_contents.append(entry[2].get())
        
        self.vocab.save_word(form_contents)
        self.new_word.new_word_win.destroy()
        self.display_vocabulary()
            

    def trigger_del_word(self, word_id):
        self.main_win.status.set("Deleting Word...")
        self.vocab.delete_word(word_id)
        self.display_vocabulary()
    

    def id_attributes(self, word_id):
        for word_object in self.vocab.vocabulary:
            if word_object.attributes["word_id"] == word_id:
                return word_object.attributes
    
    
    def trigger_import(self):
        temp_file = utils.open_file_dialog("excel_csv")

        # if file ending contains xlsx take load_excel function
        self.data_handler.load_excel(temp_file)
        self.display_vocabulary()

        # else csv, take csv read function


    def trigger_populate_file(self):
        self.file_imp = file_importer()
        self.file_imp.file_button.configure(command=self.file_loader)
        self.file_imp.submit_button.configure(command=self.save_populate_file)
    

    def file_loader(self):
        self.temp_file = utils.open_file_dialog("excel_csv")
        self.file_imp.file_entry.insert(0, self.temp_file)

    
    def save_populate_file(self):
        self.data_handler.load_excel(self.file_imp.file_entry.get())
        self.file_imp.file_imp_win.destroy()


class data_controller():
    def __init__(self, vocab):
        self.vocab = vocab

    def load_excel(self, excel_file):
        wb = load_workbook(excel_file)
        ws = wb.active
        import_dict = []
        headings = []
        for i, row in enumerate(ws.rows):
            if i == 0:
                for heading in row:
                    if heading.value != None:
                        headings.append(heading.value)
            else:
                temp_word = {}
                for i, heading in enumerate(headings):
                    if row[i].value != None:
                        temp_word[heading] = row[i].value
                import_dict.append(temp_word)
                
        self.vocab.import_words_db(import_dict)

            

    

    def load_csv(self, csv_file):
        pass




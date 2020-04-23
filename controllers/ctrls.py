import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image

from controllers import utils, log, data
from models.models import voc_model
from views.main_views import *


class lct_controller():
    def __init__(self, root, conf, start_up):
        self.conf = conf
        self.vocab = voc_model(self.conf)
        self.display_data_functions = [self.display_data, self.display_empty_data]
        self.main_win = main_frame(root, self.display_data_functions, self.vocab, self.conf)
        self.vocabulary_viewer_instances = [self.main_win.fixed_vocab_viewer]
        self.main_win.withdraw() 
        self.data_handler = data.data_controller(self.vocab, self.conf)
        self.create_voc_menu()
        self.construction_config()

        self.pos_list = self.conf.conf["part_of_speech"]

        self.start_up = start_up
        
        if self.start_up == True:
            self.load_vocabulary()
            self.start_up = False
        

    def load_vocabulary(self, name="", db_file="", metadata=[]):

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
            db_file=self.conf.conf["start_db"]
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = True
        
        self.main_win.status.set("Ready...")

        self.refresh_vocabulary()
        self.main_win.title("Language Construction Tool " + self.vocab.metadata["name"])
        
    
    def construction_config(self):
        
        for letter in self.conf.conf["consonants"]:
            self.main_win.cons_entry.insert(0, letter)
        for letter in self.conf.conf["vowels"]:
            self.main_win.vow_entry.insert(0, letter)
        for letter in self.conf.conf["special_vowels"]:
            self.main_win.spec_entry.insert(0, letter)

        self.main_win.minsize_entry.insert(0,str(2))
        self.main_win.maxsize_entry.insert(0,str(6))

        # self.main_win.cons_scale.configure(command=self.generate_wordlist)
        # self.main_win.vow_scale.configure(command=self.generate_wordlist)
        # self.main_win.spec_scale.configure(command=self.generate_wordlist)

        self.main_win.generate_button.configure(command=self.generate_wordlist)
    

    def create_voc_menu(self):

        # FILEMENU
        self.main_win.menu.add_cascade(label="File", menu=self.main_win.filemenu)
        self.main_win.filemenu.add_command(label="Create new Vocabulary", command=self.trigger_new_vocabulary)
        self.main_win.filemenu.add_command(label="Open Vocabulary...", command=self.trigger_load_vocabulary)
        self.main_win.filemenu.add_command(label="Open Recent")
        self.main_win.filemenu.add_separator()
        self.main_win.filemenu.add_command(label="Exit")

        # VOC MENU
        self.main_win.menu.add_cascade(label="Vocabulary", menu=self.main_win.vocmenu)
        self.main_win.vocmenu.add_command(label="Edit Info", command=self.trigger_update_vocabulary)
        self.main_win.vocmenu.add_command(label="Import XLS/CSV", command=self.trigger_xls_import)
        self.main_win.vocmenu.add_separator()
        self.main_win.vocmenu.add_command(label="Populate from Text...", command=self.trigger_populate_from_text)
        self.main_win.vocmenu.add_command(label="Populate from Web...", command=self.trigger_populate_from_web)
        self.main_win.vocmenu.add_separator()
        self.main_win.vocmenu.add_command(label="Export XLS/CSV/TXT")
        self.main_win.vocmenu.add_command(label="Pretty Print PDF with LaTeX")
        

        # CON MENU
        self.main_win.menu.add_cascade(label="Construction", menu=self.main_win.conmenu)
        self.main_win.conmenu.add_command(label="Export Batch...")
        self.main_win.conmenu.add_command(label="Feed File")

        # HELP MENU
        self.main_win.menu.add_cascade(label="Help", menu=self.main_win.helpmenu)
        self.main_win.helpmenu.add_command(label="Open Documentation")
        self.main_win.helpmenu.add_command(label="Info")

        # VOC BUTTONS
        
        self.main_win.voc_buttons[0].configure(command=self.trigger_new_word)
        self.main_win.clone_button.configure(command=self.trigger_vocabulary_instance)
        

    def display_data(self, event, word_object):

        self.main_win.word_header.configure(text=word_object.attributes["transliteration"])
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
        # EDIT BUTTON
        self.main_win.voc_buttons[2].configure(command=lambda wo=word_object:self.trigger_edit_word(wo))
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


    def refresh_vocabulary(self):
        # create an array for all instances of the vocabulary viewer
        # refresh all of them every time this function gets called
        
        for voc_viewer in self.vocabulary_viewer_instances:
            voc_viewer.display_vocabulary()


    def trigger_vocabulary_instance(self):
        log.debug("Creating new Instance of Vocabulary Viewer.")
        self.main_win.status.set("Creating new Instance of Vocabulary Viewer.")

        vocab_win = tk.Toplevel()
        vocab_win.minsize(300, 600)
        vocab_win.maxsize(400, 1024)
        vocab_win.title("LCT Vocab Viewer")
        vocab_win.attributes('-topmost', True)
        vocab_instance = vocab_viewer(vocab_win, self.display_data_functions, self.vocab)
        self.vocabulary_viewer_instances.append(vocab_instance)
        vocab_instance.grid(row=0, column=0, columnspan=4, rowspan=12, sticky="nsew")
        
        for i in range(12):
            vocab_win.rowconfigure(i, weight=1)
            vocab_instance.rowconfigure(i, weight=1)
            if i < 4:
                vocab_win.columnconfigure(i, weight=1)
                vocab_instance.columnconfigure(i, weight=1)
        vocab_instance.display_vocabulary()

    
    def update_related_image(self, event, word_object):
        image_filename = utils.open_file_dialog("image")
        if image_filename != "":
            self.vocab.update_word(word_object.attributes["word_id"], "related_image", utils.convertToBinaryData(image_filename))  
            self.refresh_vocabulary()
        else:
            pass

    
    def trigger_new_vocabulary(self):
        self.new_vocab = edit_vocabulary_form()
        self.new_vocab.submit_button.configure(command=self.save_new_vocabulary)
    

    def trigger_update_vocabulary(self):
        self.update_vocab = edit_vocabulary_form()
        self.update_vocab.submit_button.configure(command=self.save_update_vocabulary)

        for name, entry in self.update_vocab.entries.items():
            entry[2].insert(0, self.vocab.metadata[name])
    

    def save_update_vocabulary(self):
        self.main_win.status.set("Updating Vocabulary Metadata")
        form_contents = {}
        for name, entry in self.update_vocab.entries.items():
            form_contents[name] = entry[2].get()
        self.vocab.update_vocabulary_metadata(form_contents)
        self.update_vocab.edit_vocab_win.destroy()
        self.refresh_vocabulary()

    def save_new_vocabulary(self):
        self.main_win.status.set("Saving new Vocabulary")
        form_contents = []
        for name, entry in self.new_vocab.entries.items():
            form_contents.append(entry[2].get())
        self.load_vocabulary(name=form_contents[0], metadata=form_contents)
        self.new_vocab.edit_vocab_win.destroy()
        self.refresh_vocabulary()
        self.display_empty_data()
    

    def trigger_load_vocabulary(self):
        self.main_win.status.set("Loading Vocabulary...")
        voc_filename = utils.open_file_dialog("database")
        self.load_vocabulary(db_file=voc_filename, metadata=[])
        self.refresh_vocabulary()
        self.display_empty_data()


    def trigger_new_word(self):
        self.main_win.status.set("Opening Word Editor")
        self.temp_rel_image = ""
        self.new_word = word_form(self.pos_list)
        self.new_word.entries["related_image"][2].configure(command=self.add_related_image)
        self.new_word.submit_button.configure(command=self.save_new_word)
        

    def add_related_image(self):
        self.temp_rel_image = utils.open_file_dialog("image")
    

    def save_new_word(self):
        self.main_win.status.set("Saving New Word...")
        form_contents = {}
        for name, entry in self.new_word.entries.items():
            if name == "related_image":
                form_contents[name] = utils.convertToBinaryData(self.temp_rel_image)
            elif name == "description":
                form_contents[name] = entry[2].get("1.0",tk.END)
            elif name == "pos":
                form_contents[name] = self.new_word.default_pos.get()
            else:
                form_contents[name] = entry[2].get()
        
        self.vocab.save_word(form_contents)
        self.new_word.word_win.destroy()
        self.refresh_vocabulary()
    

    def trigger_edit_word(self, word_object):
        
        self.main_win.status.set("Opening Word Editor")
        self.temp_rel_image = ""
        self.edit_word = word_form(self.pos_list)
        self.edit_word.default_pos.set(word_object.attributes["pos"])
        self.edit_word.entries["related_image"][2].configure(command=self.add_related_image)
        self.edit_word.submit_button.configure(command=lambda w_id=word_object.attributes["word_id"]:self.update_edit_word(w_id))

        for name, entry in self.edit_word.entries.items(): 
            try:
                if name != "description":
                    entry[2].insert(0, word_object.attributes[name])
                else:
                    entry[2].insert(tk.END, word_object.attributes[name])
            except:
                pass


    def update_edit_word(self, word_id):
        self.main_win.status.set("Updating Word...")
        form_contents = {}
        for name, entry in self.edit_word.entries.items():
            if name == "related_image":
                if self.temp_rel_image != "":
                    form_contents[name] = utils.convertToBinaryData(self.temp_rel_image)
            elif name == "description":
                form_contents[name] = entry[2].get("1.0",tk.END)
            elif name == "pos":
                form_contents[name] = self.edit_word.default_pos.get()
            else:
                form_contents[name] = entry[2].get()
        
        self.vocab.update_word(form_contents, word_id)
        self.edit_word.word_win.destroy()
        self.refresh_vocabulary()
            

    def trigger_del_word(self, word_id):
        self.main_win.status.set("Deleting Word...")
        self.vocab.delete_word(word_id)
        self.refresh_vocabulary()
    

    def id_attributes(self, word_id):
        for word_object in self.vocab.vocabulary:
            if word_object.attributes["word_id"] == word_id:
                return word_object.attributes
    
    
    def trigger_xls_import(self):
        temp_file = utils.open_file_dialog("excel_csv")

        # if file ending contains xlsx take load_excel function
        self.data_handler.load_excel(temp_file)
        self.refresh_vocabulary()

        # else csv, take csv read function

    
    def save_populate_xls(self):
        self.data_handler.load_excel(self.file_imp.file_entry.get())
        self.file_imp.file_imp_win.destroy()
    

    def generate_wordlist(self):
        self.letter_parts = {}
        self.letter_parts["consonants"] = self.main_win.cons_entry.get()
        self.letter_parts["special_vowels"] = self.main_win.spec_entry.get()
        self.letter_parts["vowels"] = self.main_win.vow_entry.get()

        self.generated_word_list = self.data_handler.gen_words(self.letter_parts, 
                                            min_size=self.main_win.minsize_entry.get(), 
                                            max_size=self.main_win.maxsize_entry.get(),
                                            word_count=(self.conf.conf["construction_config"]["height"]*self.conf.conf["construction_config"]["width"])-1)

        k = 0
        for j in range(self.conf.conf["construction_config"]["width"]): #Rows
            for i in range(self.conf.conf["construction_config"]["height"]): #Columns
                self.main_win.table[k].delete(0, 'end')
                try:
                    self.main_win.table[k].insert(0, self.generated_word_list[k])
                except:
                    pass
                k += 1

    def trigger_populate_from_text(self):
        self.temp_file = ""
        self.population_window = populate_from_text()
        self.population_window.wc_entry.insert(0, 20)
        self.population_window.min_entry.insert(0, 7)
        self.population_window.max_entry.insert(0, 15)
        self.population_window.file_chooser.configure(command=self.pdf_loader)
        self.population_window.analyze_button.configure(command=self.save_populate_from_text)
    

    def pdf_loader(self):
        self.temp_file = utils.open_file_dialog("pdf")
        if self.temp_file != "":
            self.population_window.file_chooser.configure(text=self.temp_file)
    

    def save_populate_from_text(self):
        if self.temp_file != "":
            if self.population_window.config_var.get() == 1:
                population_words = self.data_handler.pdf_extractor(self.temp_file, 
                            word_count=int(self.population_window.wc_entry.get()),
                            min_size=int(self.population_window.min_entry.get()),
                            max_size=int(self.population_window.max_entry.get())
                            )
            
            self.vocab.populate_database_from_text(population_words)
            self.population_window.file_populate_win.destroy()
            self.refresh_vocabulary()
        else:
            self.population_window.warning_label.configure(text="Please choose a File!")
    

    def trigger_populate_from_web(self):
        scraper_websites = self.conf.conf["scraper_websites"]
        self.population_window = populate_from_web(scraper_websites, self.data_handler)
        self.population_window.import_button.configure(command=self.save_populate_from_web)


    def save_populate_from_web(self):
        words_list = self.data_handler.get_words_from_web(self.population_window.language_dict[self.population_window.default_language.get()], end_count=self.population_window.wc_entry.get())
        self.vocab.populate_database_from_web(words_list,
                                                    self.population_window.default_import.get(), 
                                                    self.population_window.translation_var.get())
        self.population_window.populate_web_win.destroy()
        self.refresh_vocabulary()



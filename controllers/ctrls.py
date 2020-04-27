import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image
from timeit import default_timer as timer

from controllers import utils, log, data
from models.models import voc_model
from views.main_views import *

class lct_controller():
    def __init__(self, root, conf):
        self.conf = conf.conf
        self.vocab = voc_model(self.conf)
        self.display_data_functions = [self.display_data, self.display_empty_data]
        self.main_win = main_frame(root, self.display_data_functions, self.vocab, self.conf)
        self.vocabulary_viewer_instances = [self.main_win.fixed_vocab_viewer]
        self.main_win.withdraw() 
        self.data_handler = data.data_controller(self.vocab, self.check_for_duplicates)
        self.populate_menu()
        self.construction_config()

        self.pos_list = self.conf["part_of_speech"]
        self.bind_keys(root)
        self.load_vocabulary()
    

    def load_vocabulary(self, name="", db_file="", metadata=[]):
        start = timer()
        if name != "" and metadata != [] and db_file == "":
            self.main_win.status.set("Creating new Vocabulary...")
            log.debug("CTRL: Creating new Vocabulary.")
            db_file = "data/" + utils.string_unify(name) + ".db"
            self.vocab.load_db(db_file=db_file, metadata=metadata, mode="create")
            self.show_tooltips = False
        elif name == "" and metadata == [] and db_file != "":
            self.main_win.status.set("Loading Vocabulary {}".format(db_file))
            log.debug("Loading Vocabulary {}".format(db_file))
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = False
        else:
            self.main_win.status.set("Loading Start Vocabulary")
            log.debug("CTRL: Loading Start Vocabulary")
            db_file=self.conf["start_db"]
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = True
        
        self.main_win.status.set("Ready...")

        self.refresh_vocabulary()
        end = timer()
        # print(end - start)
        self.main_win.title("Language Construction Tool " + self.vocab.metadata["name"])
        
    
    def construction_config(self):
        
        insert_cons = str(self.conf["consonants"]).replace("'","").replace("[", "").replace("]", "").replace(" ", "")
        insert_vow = str(self.conf["vowels"]).replace("'","").replace("[", "").replace("]", "").replace(" ", "")
        insert_spec = str(self.conf["special_vowels"]).replace("'","").replace("[", "").replace("]", "").replace(" ", "")
        self.main_win.cons_entry.insert(0, insert_cons)
        self.main_win.vow_entry.insert(0, insert_vow)
        self.main_win.spec_entry.insert(0, insert_spec)

        self.main_win.minsize_entry.insert(0,str(2))
        self.main_win.maxsize_entry.insert(0,str(6))

        self.main_win.hardness_scale.configure(command=self.generate_wordlist)
        self.main_win.foreign_scale.configure(command=self.generate_wordlist)

        self.main_win.generate_button.configure(command=lambda value=0:self.generate_wordlist(0))
        self.main_win.export_button.configure(command=self.save_export_batch)


    def populate_menu(self):

        # FILEMENU
        self.main_win.menu.add_cascade(label="File", menu=self.main_win.filemenu)
        self.main_win.filemenu.add_command(label="Create new Vocabulary", command=self.trigger_new_vocabulary)
        self.main_win.filemenu.add_command(label="Open Vocabulary...", command=self.trigger_load_vocabulary)
        # self.main_win.filemenu.add_command(label="Open Recent")
        self.main_win.filemenu.add_separator()
        self.main_win.filemenu.add_command(label="Exit")

        # VOC MENU
        self.main_win.menu.add_cascade(label="Vocabulary", menu=self.main_win.vocmenu)
        self.main_win.vocmenu.add_command(label="Edit Info", command=self.trigger_update_vocabulary)
        self.main_win.vocmenu.add_command(label="Import CSV/XLS", command=self.trigger_xls_import)
        self.main_win.vocmenu.add_separator()
        self.main_win.vocmenu.add_command(label="Populate from Text...", command=self.trigger_populate_from_text)
        self.main_win.vocmenu.add_command(label="Populate from Web...", command=self.trigger_populate_from_web)
        self.main_win.vocmenu.add_separator()
        self.main_win.vocmenu.add_command(label="Export Vocabulary...", command=self.trigger_export_vocabulary)

        # GEN MENU
        # self.main_win.menu.add_cascade(label="Generation", menu=self.main_win.genmenu)
        # self.main_win.genmenu.add_command(label="Export Batch...", command=self.trigger_export_batch)
        # self.main_win.genmenu.add_command(label="Feed File")

        # HELP MENU
        self.main_win.menu.add_cascade(label="Help", menu=self.main_win.helpmenu)
        # self.main_win.helpmenu.add_command(label="Open Documentation")
        self.main_win.helpmenu.add_command(label="Info", command=self.trigger_info_window)

        # VOC BUTTONS
        
        self.main_win.voc_buttons[0].configure(command=self.trigger_new_word)
        self.main_win.clone_button.configure(command=self.trigger_vocabulary_instance)
        

    def bind_keys(self, root):
        root.bind("<Control-n>", lambda event: self.trigger_new_word())
        root.bind("<Control-v>", lambda event: self.trigger_new_vocabulary())
        root.bind("<Delete>", lambda event: self.trigger_del_word())
        root.bind("<Control-i>", lambda event: self.trigger_xls_import())
        root.bind("<Control-e>", lambda event: self.trigger_export_vocabulary())
        root.bind("<F5>", lambda event: self.refresh_vocabulary())


    def display_data(self, event, word_):

        self.main_win.word_header.configure(text=word_["transliteration"])
        self.main_win.phonetics_label.configure(text=word_["phonetics"])
        self.main_win.pos_label.configure(text=word_["pos"])
        self.main_win.translation_label.configure(text=word_["translation"])
        self.main_win.example_label.configure(text=word_["example_sentence"])
        self.main_win.example_translation_label.configure(text=word_["example_translation"])
        self.main_win.description.set_html(html=word_["description"])
        img = word_["related_image"]
        self.main_win.related_image.image = ImageTk.PhotoImage(img.resize((200, 200), Image.ANTIALIAS))
        self.main_win.related_image.create_image(0, 0, image=self.main_win.related_image.image, anchor='nw')
        self.main_win.related_image.bind('<Double-Button-1>', lambda event, wo=word_: self.update_related_image(event, wo))
        # DELETE BUTTON
        self.main_win.voc_buttons[1].configure(command=self.trigger_del_word)
        # EDIT BUTTON
        self.main_win.voc_buttons[2].configure(command=lambda wo=word_:self.trigger_edit_word(wo))
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


    def refresh_vocabulary(self, event=None):
        # create an array for all instances of the vocabulary viewer
        # refresh all of them every time this function gets called
        self.main_win.status.set("Ready...")
        for voc_viewer in self.vocabulary_viewer_instances:
            voc_viewer.display_vocabulary()


    def trigger_vocabulary_instance(self):
        log.debug("Creating new Instance of Vocabulary Viewer.")
        self.main_win.status.set("Creating new Instance of Vocabulary Viewer.")
        vocab_win = common_win(main_win=False)
        vocab_win.toplevel_win.minsize(300, 600)
        vocab_win.toplevel_win.maxsize(400, 1024)
        vocab_win.toplevel_win.title("LCT Vocab Viewer")
        vocab_instance = vocab_viewer(vocab_win.toplevel_win, self.display_data_functions, self.vocab)
        self.vocabulary_viewer_instances.append(vocab_instance)
        vocab_instance.grid(row=0, column=0, columnspan=4, rowspan=12, sticky="nsew")
        
        for i in range(12):
            vocab_win.toplevel_win.rowconfigure(i, weight=1)
            vocab_instance.rowconfigure(i, weight=1)
            if i < 4:
                vocab_win.toplevel_win.columnconfigure(i, weight=1)
                vocab_instance.columnconfigure(i, weight=1)
        vocab_instance.display_vocabulary()

    
    def update_related_image(self, event, word_):
        self.main_win.status.set("Updating Related Image...")
        image_filename = utils.open_file_dialog("image")
        log.debug("CTRL: Updating Related Image with {}".format(image_filename))
        if image_filename != "":
            self.vocab.update_word(word_["word_id"], "related_image", utils.convertToBinaryData(image_filename))  
            self.refresh_vocabulary()
            self.main_win.status.set("Ready...")
        else:
            pass

    
    def trigger_new_vocabulary(self, event=None):
        log.debug("CTRL: Creating new vocabulary.")
        self.main_win.status.set("Creating new Vocabulary...")
        self.new_vocab = edit_vocabulary_form()
        self.new_vocab.submit_button.configure(command=self.save_new_vocabulary)
    

    def trigger_update_vocabulary(self):
        log.debug("CTRL: Updating Vocabulary.")
        self.main_win.status.set("Updating Vocabulary...")

        self.update_vocab = edit_vocabulary_form()
        self.update_vocab.submit_button.configure(command=self.save_update_vocabulary)

        for name, entry in self.update_vocab.entries.items():
            entry[2].insert(0, self.vocab.metadata[name])
    

    def save_update_vocabulary(self):
        form_contents = {}
        for name, entry in self.update_vocab.entries.items():
            form_contents[name] = entry[2].get()
        self.vocab.update_vocabulary_metadata(form_contents)
        self.update_vocab._quit()
        self.refresh_vocabulary()


    def save_new_vocabulary(self):
        self.main_win.status.set("Saving new Vocabulary")
        form_contents = []
        for name, entry in self.new_vocab.entries.items():
            form_contents.append(entry[2].get())
        self.load_vocabulary(name=form_contents[0], metadata=form_contents)
        self.new_vocab._quit()
        self.refresh_vocabulary()
        self.display_empty_data()
    

    def trigger_load_vocabulary(self):
        self.main_win.status.set("Loading Vocabulary...")
        voc_filename = utils.open_file_dialog("database")
        self.load_vocabulary(db_file=voc_filename, metadata=[])
        self.refresh_vocabulary()
        self.display_empty_data()


    def trigger_new_word(self, event=None):
        log.debug("CTRL: Creating new word...")
        self.main_win.status.set("Creating new word...")
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
                duplicate_check = self.check_for_duplicates(entry[2].get(), heading_list=["transliteration", "translation"])
                if duplicate_check != True:
                    MsgBox = tk.messagebox.askquestion ('Found Duplicate','Word already exists: {}. Do wish to continue?'.format(duplicate_check),icon = 'warning')
                    if MsgBox == True:
                        self.vocab.save_word(form_contents)
                        self.new_word._quit()
                        self.refresh_vocabulary()
                        return
                    else:
                        self.new_word._quit()
                        return
                else:
                    pass
        
        self.vocab.save_word(form_contents)
        self.new_word._quit()
        self.refresh_vocabulary()


    def check_for_duplicates(self, term, heading_list=[]):
        if term != "-" and term != " ":
            checker = ""
            if self.vocab.vocabulary != []:
                for heading in heading_list:
                    for word in self.vocab.vocabulary:   
                        if word[heading] == term: 
                            checker = term 
                            return checker   
                        else:
                            checker = True
                    
            else:
                checker = True
        else: 
            checker = True
        
        return checker    


    def trigger_edit_word(self, word_):
        log.debug("CTRL: Updating {}".format(word_["transliteration"]))
        self.main_win.status.set("Updating Word...")
        self.temp_rel_image = ""
        self.edit_word = word_form(self.pos_list)
        self.edit_word.default_pos.set(word_["pos"])
        self.edit_word.entries["related_image"][2].configure(command=self.add_related_image)
        self.edit_word.submit_button.configure(command=lambda w_id=word_["word_id"]:self.update_edit_word(w_id))

        self.temp_word = word_
        
        for name, entry in self.edit_word.entries.items(): 
            try:
                if name != "description":
                    entry[2].insert(0, word_[name])
                else:
                    entry[2].insert(tk.END, word_[name])
            except:
                pass


    def update_edit_word(self, word_id):
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
                if entry[2].get() != self.temp_word["transliteration"] and entry[2].get() != self.temp_word["translation"]:
                    duplicate_check = self.check_for_duplicates(entry[2].get(), heading_list=["transliteration", "translation"])
                    if duplicate_check != True:
                        MsgBox = tk.messagebox.askquestion ('Found Duplicate','Word already exists: {}. Do wish to continue?'.format(duplicate_check),icon = 'warning')
                        if MsgBox == True:
                            self.vocab.update_word(form_contents, word_id)
                            self.edit_word._quit()
                            self.refresh_vocabulary()
                            return
                        else:
                            self.edit_word._quit()
                            return
                    else:
                        pass
        
        self.vocab.update_word(form_contents, word_id)
        self.edit_word._quit()
        self.refresh_vocabulary()
            

    def trigger_del_word(self, event=None):
        # self.main_win.status.set("Deleting Word...")
        treeview = self.main_win.fixed_vocab_viewer.word_list
        selection = treeview.selection()
        word_ids = []
        for sel_ in selection:
            word_ids.append((treeview.item(sel_)['tags'][0],))
        self.vocab.delete_word(word_ids)
        self.refresh_vocabulary()
    

    def id_attributes(self, word_id):
        for word_ in self.vocab.vocabulary:
            if word_["word_id"] == word_id:
                return word_
    
    
    def trigger_xls_import(self, event=None):
        self.main_win.status.set("Importing Excel File...")
        temp_file = utils.open_file_dialog("excel_csv")

        if temp_file[-4:] == "xlsx":
            self.data_handler.load_excel(excel_file=temp_file)

        elif temp_file[-3:] == "csv":
            self.data_handler.load_excel(csv_file=temp_file)
        
        self.refresh_vocabulary()


    def generate_wordlist(self, value):
        self.letter_parts = {}
        self.letter_parts["consonants"] = self.main_win.cons_entry.get().split(",")
        self.letter_parts["special_vowels"] = self.main_win.spec_entry.get().split(",")
        self.letter_parts["vowels"] = self.main_win.vow_entry.get().split(",")

        generated_word_list = self.data_handler.gen_words(self.letter_parts, 
                                            min_size=self.main_win.minsize_entry.get(), 
                                            max_size=self.main_win.maxsize_entry.get(),
                                            word_count=(self.conf["construction_config"]["height"]*self.conf["construction_config"]["width"])-1,
                                            foreigness=self.main_win.foreign_scale.get(),
                                            hardness=self.main_win.hardness_scale.get())

        k = 0
        for j in range(self.conf["construction_config"]["width"]): #Rows
            for i in range(self.conf["construction_config"]["height"]): #Columns
                self.main_win.table[k].delete(0, 'end')
                try:
                    self.main_win.table[k].insert(0, generated_word_list[k])
                except:
                    pass
                k += 1


    def trigger_populate_from_text(self):
        self.main_win.status.set("Populating Vocabulary from Text...")
        self.temp_file = ""
        self.population_window = populate_from_text()
        self.population_window.wc_entry.insert(0, 20)
        self.population_window.min_entry.insert(0, 7)
        self.population_window.max_entry.insert(0, 15)
        self.population_window.file_chooser.configure(command=self.text_loader)
        self.population_window.analyze_button.configure(command=self.save_populate_from_text)
    

    def text_loader(self):
        self.temp_file = utils.open_file_dialog("text")
        if self.temp_file != "":
            self.population_window.file_chooser.configure(text=self.temp_file)
    

    def save_populate_from_text(self):
        if self.temp_file != "":      
            if self.population_window.config_var.get() == 1:
                population_words = self.data_handler.text_extractor(self.temp_file, 
                            word_count=int(self.population_window.wc_entry.get()),
                            min_size=int(self.population_window.min_entry.get()),
                            max_size=int(self.population_window.max_entry.get())
                            )
                match_count = []
                for population_word in population_words:
                    duplicate_check = self.check_for_duplicates(population_word, heading_list=["translation"])
                    if duplicate_check != True:
                        match_count.append(population_word)
                    else:
                        pass
                if match_count != []:
                    message_ = '''Found {} words, which are already in vocabulary. Import anyway?
                                    Press YES to import all. 
                                    Press NO to import all without duplicates.
                                    Press CANCEL to abort.
                                    '''.format(str(len(match_count)))
                    self.population_window._quit()
                    MsgBox = tk.messagebox.askyesnocancel("Found Duplicates", message_)
                    print(MsgBox)
                    if MsgBox == True:
                        self.vocab.populate_database_from_text(population_words) 
                        self.refresh_vocabulary()
                        return
                    elif MsgBox == False:
                        for match in match_count:
                            population_words.remove(match)
                        self.vocab.populate_database_from_text(population_words)
                        self.refresh_vocabulary()
                        return

                    else:
                        return
                
                else:
                    self.vocab.populate_database_from_text(population_words)
                    self.population_window._quit()
                    self.refresh_vocabulary()
                    return


        else:
            self.population_window.warning_label.configure(text="Please choose a File!")
    

    def trigger_populate_from_web(self):
        self.main_win.status.set("Populating Vocabulary from Web...")
        scraper_websites = self.conf["scraper_websites"]
        self.population_window = populate_from_web(scraper_websites, self.data_handler)
        self.population_window.import_button.configure(command=self.save_populate_from_web)


    def save_populate_from_web(self):
        words_list = self.data_handler.get_words_from_web(self.population_window.language_dict[self.population_window.default_language.get()], 
                                                        start_count=self.population_window.start_count.get(), 
                                                        end_count=self.population_window.end_count.get())
        match_count = []
        for import_word in words_list:
            duplicate_check = self.check_for_duplicates(import_word["translation"], heading_list=["transliteration","translation"])
            if duplicate_check != True:
                match_count.append(import_word)
            else:
                pass
        if match_count != []:
            message_ = '''Found {} words, which are already in vocabulary. Import anyway?
                            Press YES to import all. 
                            Press NO to import all without duplicates.
                            Press CANCEL to abort.
                            '''.format(str(len(match_count)))
            self.population_window._quit()
            MsgBox = tk.messagebox.askyesnocancel("Found Duplicates", message_)

            if MsgBox == True:
                self.vocab.populate_database_from_web(words_list,
                                                            self.population_window.default_import.get(), 
                                                            self.population_window.translation_var.get())
                self.refresh_vocabulary()
                return
            
            elif MsgBox == False:
                for match in match_count:
                    words_list.remove(match)
                self.vocab.populate_database_from_web(words_list,
                                                            self.population_window.default_import.get(), 
                                                            self.population_window.translation_var.get())
                self.refresh_vocabulary()
                return

            else:
                return
        else:
            self.vocab.populate_database_from_web(words_list,
                                                        self.population_window.default_import.get(), 
                                                        self.population_window.translation_var.get())
            self.population_window._quit()
            self.refresh_vocabulary()
            return 


    def trigger_export_vocabulary(self, event=None):
        self.main_win.status.set("Exporting Vocabulary...")
        format_list=["CSV", "XLSX"]
        self.export_window = export_vocabulary(format_list, self.conf["word_attributes"])
        self.export_window.export_button.configure(command=self.save_export_vocabulary)

    
    def save_export_vocabulary(self):    
        filename = filedialog.asksaveasfilename(initialdir = "/data",title = "Save as...",filetypes = (("all files","*.*"),))

        column_indexes = self.export_window.column_chooser.curselection()  
        columns = []        
        for index in column_indexes:
            columns.append(self.export_window.column_chooser.get(index))

        format_indexes = self.export_window.format_chooser.curselection()  
        formats = []        
        for index in format_indexes:
            formats.append(self.export_window.format_chooser.get(index))

        self.data_handler.export_vocabulary_as_file(filename, self.vocab.vocabulary, formats, columns)
        self.main_win.status.set("Ready...")
        self.export_window._quit()
    

    def save_export_batch(self):
        filetypes= (("xlsx files","*.xlsx"), ("csv files","*.csv"), ("docx files","*.docx"), ("txt files","*.txt"))
        filename = filedialog.asksaveasfilename(initialdir = "/data",title = "Export as...", filetypes = filetypes, defaultextension="*.txt")

        self.letter_parts = {}
        self.letter_parts["consonants"] = self.main_win.cons_entry.get().split(",")
        self.letter_parts["special_vowels"] = self.main_win.spec_entry.get().split(",")
        self.letter_parts["vowels"] = self.main_win.vow_entry.get().split(",")

        generated_word_list = self.data_handler.gen_words(self.letter_parts, 
                                            min_size=self.main_win.minsize_entry.get(), 
                                            max_size=self.main_win.maxsize_entry.get(),
                                            word_count=int(self.main_win.wc_entry.get()),
                                            foreigness=self.main_win.foreign_scale.get(),
                                            hardness=self.main_win.hardness_scale.get())
                                
        self.data_handler.export_batch(generated_word_list, filename)
        self.main_win.status.set("Ready...")

    
    def trigger_info_window(self):
        info_win = info_window()


import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image
import io


from controllers import utils
from controllers import log
from models.models import voc_model
from views.main_views import *


class lct_controller():
    def __init__(self, root, start_up):
        self.vocab = voc_model()
        self.main_win = main_frame(root)
        self.main_win.withdraw() 
        self.create_voc_menu()

        self.start_up = start_up
        
        if self.start_up == True:
            self.load_vocabulary()
            self.start_up = False
    
    def load_vocabulary(self, name="", db_file="", metadata=[]):
        self.vocab = voc_model()

        if name != "" and metadata != [] and db_file == "":
            db_file = "data/" + utils.string_unify(name) + ".db"
            self.vocab.load_db(db_file=db_file, metadata=metadata, mode="create")
            self.show_tooltips = False
        elif name == "" and metadata == [] and db_file != "":
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = False
        else:
            db_file="data/new_test.db"
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = True

        self.display_vocabulary()
        self.main_win.title("Language Construction Tool " + self.vocab.metadata["name"])
        

    def display_vocabulary(self):
        self.main_win.word_list.delete(*self.main_win.word_list.get_children())
        for word_object in self.vocab.vocabulary:
            self.main_win.word_list.insert("", "end", text=word_object.attributes["word"], values=word_object.attributes["translation"], tags=(word_object.attributes["word_id"],))
            self.main_win.word_list.tag_bind(word_object.attributes["word_id"],'<<TreeviewSelect>>', lambda event, wo=word_object: self.display_data(event, wo))
        self.focus_object(self.main_win.word_list)
        
    
    def create_voc_menu(self):
        # Add some commands
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Create new Vocabulary", command=self.trigger_new_vocabulary)
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Open Vocabulary", command=self.trigger_load_vocabulary)
        self.main_win.voc_menu_buttons[0].menu.add_separator()
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Populate from File...")
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Populate from Web...")
        self.main_win.voc_menu_buttons[0].menu.add_separator()
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Exit")
        self.main_win.voc_menu_buttons[1].configure(command=self.trigger_new_word)
        

    def display_data(self, event, word_object):
        # print(word_object.attributes["word_id"])
        for element in self.main_win.gui_displays:
            element[0].configure(text=word_object.attributes[element[3]])
            element[0].bind('<Double-Button-1>', 
            lambda event, ele=element, wo=word_object: self.editor_switch(event, 
                                            ele, 
                                            False, 
                                            wo))

        self.main_win.description_header.set_html(html=word_object.attributes["description"])
        self.main_win.description_header.bind('<Double-Button-1>', lambda event, wo=word_object: self.edit_description(event, wo))

        img = word_object.attributes["related_image"]
   
        self.main_win.related_image.image = ImageTk.PhotoImage(img, Image.ANTIALIAS)     
        self.main_win.related_image.create_image(0, 0, image=self.main_win.related_image.image, anchor='nw')
        self.main_win.related_image.bind('<Double-Button-1>', lambda event, wo=word_object: self.update_related_image(event, wo))
        self.main_win.voc_menu_buttons[2].configure(command=lambda word_id=word_object.attributes["word_id"]:self.trigger_del_word(word_id))
        try:
            row = 1
            for i, rel_id in enumerate(word_object.attributes["related_words"]):
                rel_word = self.id_attributes(rel_id)
                tk.Label(self.main_win.rel_words_frame, text=rel_word["word"]).grid(row=row, column=i, sticky="nse")
                if i%3 == 0:
                    row += 1
        except TypeError:
            pass
        self.main_win.rel_words_header.bind('<Double-Button-1>', lambda event, wo=word_object: self.trigger_rel_editor(event, wo))


    def display_empty_data(self):
        for element in self.main_win.gui_displays:
            element[0].configure(text="")

        self.main_win.description_header.set_html(html="")
        img = Image.new('RGB', (500, 1080), (228, 150, 150))
   
        self.main_win.related_image.image = ImageTk.PhotoImage(img)     
        self.main_win.related_image.create_image(0, 0, image=self.main_win.related_image.image, anchor='nw')


    def editor_switch(self, event, element, switch, word_object, save=False):
        log.debug("GUI: Switch triggered for " + element[3])
        if switch == True and save == True:
            self.vocab.update_word(word_object.attributes["word_id"], 
                                    element[3], 
                                    element[switch].get())

        element[switch].grid_forget()
        element[not switch].grid(column=element[2][0], 
                                row=element[2][1], 
                                sticky=element[2][2])
        try:
            element[not switch].delete(0, tk.END)
            element[not switch].insert(0,element[switch]["text"])
            element[not switch].bind("<Return>", 
                                    lambda event, elem=element, wo=word_object:self.editor_switch(event, 
                                                                    elem, 
                                                                    True, 
                                                                    wo,
                                                                    save=True))

            element[not switch].bind("<Escape>", 
                                    lambda event, elem=element, wo=word_object:self.editor_switch(event, 
                                                                    elem, 
                                                                    True, 
                                                                    wo,
                                                                    save=False))
        except:
            pass
        self.display_vocabulary()


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
        form_contents = []
        for name, entry in self.new_vocab.entries.items():
            form_contents.append(entry[2].get())
        self.load_vocabulary(name=form_contents[0], metadata=form_contents)
        self.new_vocab.new_vocab_win.destroy()
        self.display_vocabulary()
        self.display_empty_data()
    
    def trigger_load_vocabulary(self):
        voc_filename = utils.open_file_dialog("database")
        self.load_vocabulary(db_file=voc_filename, metadata=[])
        self.display_vocabulary()
        self.display_empty_data()


    def trigger_new_word(self):
        self.temp_rel_image = ""
        word_list = []
        if self.vocab.vocabulary != []:
            for word_object in self.vocab.vocabulary:
                word_list.append(word_object.attributes["word"])
        else:
            word_list = False
    
        self.new_word = new_word_form(word_list)
        self.new_word.entries["rel_image"][2].configure(command=self.add_related_image)
        self.new_word.submit_button.configure(command=self.save_new_word)

        

    def add_related_image(self):
        self.temp_rel_image = utils.open_file_dialog("image")
    

    def save_new_word(self):
        related_words = []
        for key, value in self.new_word.word_to_button.items():
            related_words.append(key)
       
        form_contents = []
        for name, entry in self.new_word.entries.items():
            if name == "rel_image":
                form_contents.append(utils.convertToBinaryData(self.temp_rel_image))
            elif name == "rel_words":
                form_contents.append(related_words)
            elif name == "description":
                form_contents.append(entry[2].get("1.0",tk.END))
            else:
                form_contents.append(entry[2].get())
        
        self.vocab.save_word(form_contents)
        self.new_word.new_word_win.destroy()
        self.display_vocabulary()
            

    def trigger_del_word(self, word_id):
        self.vocab.delete_word(word_id)
        self.display_vocabulary()
    

    def id_attributes(self, word_id):
        for word_object in self.vocab.vocabulary:
            if word_object.attributes["word_id"] == word_id:
                return word_object.attributes
    
    
    def trigger_rel_editor(self, event, word_object):
        print(word_object.attributes["word"])
        word_list = []
        if self.vocab.vocabulary != []:
            for word_object in self.vocab.vocabulary:
                word_list.append(word_object.attributes["word"])
        else:
            word_list = False
        
        rel_words = []
        print(word_object.attributes["related_words"])
        for rel_id in word_object.attributes["related_words"]:
            word_name = self.id_attributes(rel_id)
            rel_words.append(word_name["word"])
        
        print(rel_words)
        
        self.rel_editor = rel_word_editor(word_list, rel_words)
        self.rel_editor.submit_button.configure(command=lambda word_id= word_object.attributes["word_id"]: self.save_rel_editor(word_id))


    def save_rel_editor(self, word_id):
        related_words = []
        for key, value in self.rel_editor.word_to_button.items():
            related_words.append(key)
        self.vocab.save_rel_words(related_words, word_id)

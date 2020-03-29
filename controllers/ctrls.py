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

        self.start_up = start_up
        
        if self.start_up == True:
            self.load_vocabulary()
            self.start_up = False
    
    def load_vocabulary(self, name="", db_file=""):
        self.vocab = voc_model()

        if name != "" and db_file == "":
            db_file = "data/" + name + ".db"
            self.vocab.load_db(db_file, mode="create")
            self.show_tooltips = False
        elif name == "" and db_file != "":
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = False
        else:
            db_file="data/start.db"
            self.vocab.load_db(db_file, mode="load")
            self.show_tooltips = True

        self.display_vocabulary()
        

    def display_vocabulary(self):
        self.main_win.word_list.delete(*self.main_win.word_list.get_children())
        for i, word_object in enumerate(self.vocab.vocabulary):
            # print(word_object.attributes["word"])
            self.main_win.word_list.insert("", i, text=word_object.attributes["word"], values=word_object.attributes["translation"], tags=(word_object.attributes["word"]))
            self.main_win.word_list.tag_bind(word_object.attributes["word"],'<<TreeviewSelect>>', lambda event: self.display_data(event, word_object))
            self.focus_object(self.main_win.word_list)
        
        # Add some commands
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Create new Vocabulary", command=self.trigger_new_vocabulary)
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Open Vocabulary")
        self.main_win.voc_menu_buttons[0].menu.add_separator()
        self.main_win.voc_menu_buttons[0].menu.add_command(label="Exit")


    def display_data(self, event, word_object):
        for element in self.main_win.gui_displays:
            element[0].configure(text=word_object.attributes[element[3]])
            element[0].bind('<Double-Button-1>', 
            lambda event: self.editor_switch(event, 
                                            element, 
                                            False, 
                                            word_object))

        self.main_win.description_header.set_html(html=word_object.attributes["description"])
        self.main_win.description_header.bind('<Double-Button-1>', lambda event: self.edit_description(event, word_object))

        img = word_object.attributes["related_image"]
   
        self.main_win.related_image.image = ImageTk.PhotoImage(img, Image.ANTIALIAS)     
        self.main_win.related_image.create_image(0, 0, image=self.main_win.related_image.image, anchor='nw')
        self.main_win.related_image.bind('<Double-Button-1>', lambda event: self.update_related_image(event, word_object))


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
                                    lambda event:self.editor_switch(event, 
                                                                    element, 
                                                                    True, 
                                                                    word_object,
                                                                    save=True))

            element[not switch].bind("<Escape>", 
                                    lambda event:self.editor_switch(event, 
                                                                    element, 
                                                                    True, 
                                                                    word_object,
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
        image_filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.vocab.update_word(word_object.attributes["word_id"], "related_image", utils.convertToBinaryData(image_filename))
        self.display_vocabulary()

    
    def trigger_new_vocabulary(self):
        self.new_vocab = new_vocabulary()

        
        


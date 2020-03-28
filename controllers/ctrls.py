import tkinter as tk
from tkinter import ttk
from functools import partial

from controllers import utils
from controllers import log
from models.models import voc_model
from views.main_views import main_frame


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
            self.main_win.word_list.insert("", i, text=word_object.attributes["word"], tags=(word_object.attributes["word"]))
            self.main_win.word_list.tag_bind(word_object.attributes["word"],'<<TreeviewSelect>>', lambda event: self.display_data(event, word_object))
            self.focus_object(self.main_win.word_list)


    def display_data(self, event, word_object):
        for element in self.main_win.gui_displays:
            element[0].configure(text=word_object.attributes[element[3]])
            element[0].bind('<Double-Button-1>', 
            lambda event: self.editor_switch(event, 
                                            element, 
                                            False, 
                                            word_object))


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

        
        


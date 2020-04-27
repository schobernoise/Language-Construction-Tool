# Language Construction Tool

![The Language Construction Tool](http://www.fabianschober.com/assets/lct/lct.jpg)

## Release Notes

Welcome to the Language Construction Tool (LCT)! As you will probably have guessed, this tool is designed to help you keep track of your work with languages. This could mean several things like:

- Designing/constructing a language (conlanging)
- Learning a language
- Keeping track of a professional Vocabulary (Terms)

Of course you can configure this tool to fit your needs however you like. For example, with some small adjustments you could use it as database-manager for recipes and so on.

## Prerequisites and Quickstart

This tools entire GUI is based on tkinter.
Everything is tested and developed on Python 3.8.
I highly recommend working with a virtual environment, especially due to the many dependencies.

You can check out the venv-module [here](https://docs.python.org/3/tutorial/venv.html).

Once you have setup the venv, just install the requirements.txt via pip.

`pip install -r requirements.txt`

Now you should be good to go! With your venv enabled, run 

`python app.py`

With first starting this program, it will build the "config.yaml" and "start.db".

## Config

- *log_level:* WARNING, DEBUG; INFO or ERROR (Which will be displayed in the CL)
- *part_of_speech, word_attributes and vocabulary_metadata:*
This program is built around the config.yaml for more flexibility. The idea was, that if you change one word_attribute, everything would change and you could remodel the whole program to somethign completely different with a few clicks.
But some parts are still hardcoded, so I would leave that for now as is. 
- *start_db:* Which Database will be loaded on startup.
- *consonants, vowels and special_vowels:* Letters which will be loaded in the generator on startup.
- *construction_config:* The dimensions of the generated word table.
- *scraper_websites:* Websites which can be used as Word sources. I have implemented one so far,
but feel free to share your input!

## Usage and Best Practices

First, unzip the "ressources.zip" and have a look inside.
The Language Construction Tool comes with a sample Vocabulary to import, to demonstrate some of its key functionality.

When you open up the "sample_vocabulary.xlsx", you will see that there are several headings, which are identical to the headings found in the "config_yaml". And the column for the "related_images" is empty. This is no mistake. If there is a column for related images, you can place your images, numbered identical to its corresponding word in a folder near the sheet, like you find here. There have not to be images for all words.

Get back to our LCT and click on File - "Create new Vocabulary". A new Window pops up and asks for some information. With "translation language" is meant the language that you speak/ translate the constructed language into. So if you speak e.g. German, write German.
Then hit "Submit Vocabulary". Congratulations, you now have created a blank Vocabulary!
All new Vocabularies will be saved in the "data"-folder.

Go to Vocabulary - "Import CSV/XLS". A filebrowser comes up. Choose the right extension and search for our excel sheet. Hit "Open".

When you now navigate via clicking the words on the left side, you are able to obtain all information you also found in the excel sheet. This way it is possible to import large quantitities of words, e.g. you have already started constructing and want to continue with the LCT.

You can add a new word with the button "add" on the lower left. A window comes up, which enables you to make an entry for a new word. It should be pretty self explanatory.

The same goes for the "edit" and "delete" button.

Now to some of the advanced methods!

Click on "Clone Vocabulary Viewer" and obtain another instance of the viewer. You can have as many instances as you like. When you now click on the little up arrow a few times right over the treeview of one vocabulary viewer you will see that it only shows the selected part of speech words. You can now seperately do this for all of the viewers and compare lists, also with the search bar.

![Different Vocabulary Viewers](http://www.fabianschober.com/assets/lct/vocab_viewers.jpg)

Now click on Vocabulary - "Populate from Text". This function comes in handy when you want to build your language areound a specific topic, e.g. a language for a people who are great sailors. You can pick some texts about the nautical trade and say that you like to pick the 100 most used words with a min_length of 10. Now you have a lot of nautical terms to work with!
In our case I picked something from archive.org, the International Journal of Computer Science and Information Security (IJCSIS) Vol. 15, No. 12, December 2017. Go ahead and try it out!
Your vocabulary now should have a lot more words to work with.

Next hit Vocabulary - Populate from Web. 
This function has basically the same idea, but instead of texts it uses a web-scraper. There is currently only one website implemented, though I found it suited my needs already. The option "import as" is for e.g. when you learn a language and, so you can import the words of this langauge as transliteration, and the english translation as translation. This way you could use the program to learn an existing language.

"Start Index" and "End Index" are for picking which of the 1000 most common words should be imported. Now hit "Import Words!"

You will prompted when duplicates are found.

If you want to export your vocabulary, you can do this via Vocabulary - "Export Vocabulary". Choose your formats, which columns and hit "Export".

On the upper right side of the main win you will see another tab "Generation". This is not a "Language Generator", but mereley a tool to combine letters in probabilistic ways, so it helps you assemble them to words. Everything seperated by a coma will be used as one letter, so you could also use items like "ah", "ch", "ck" and so on.

If you would like to take a list of generated words with you, you can just export them! Choose how many, and hit "Export Batch!".


**Keybindings**

- Ctrl+N: New Word
- Ctrl+V: New Vocabulary
- Ctrl+I: Import XLSX/CSV
- Ctrl+E: Export Vocabulary as XLSX/CSV
- F5: Refresh Vocabulary
- Del: Delete selected words


## Known Bugs
- Word generator generates not exactly the word_count entered, due to its removal of duplicates (creates set of generated words).


# Plans for the Future

**Minor Features/Fixes**
- Make Recent Vocabulary Menu Entry
- Make Generate exactly as much words as needed
- Export Images in Excel Sheet
- Strg+A: Select all words
- related_image Importer from file supports more formats


**Make whole codestructure follow config headers**

**Example Sentences**
Make Infos fill in automatically with Linguee
https://github.com/imankulov/linguee-api

**Asynchronous Tasks**

**Pretty Print Feature**
Print Vocabulary Duden Style as PDF

**API**
- Make a CLI-script for API purposes
- Generating words with given parameters
- Accessing the database

**Generation**
- User can pick from different combination algorithms.
- Feed text from file, generates words based on the language in it.

**Related Words**

- User gets to choose which words related to each other.
- Relations work two ways in Database


**Visualization Tab**
- Tools to visualize the users vocabulary

**Handwriting Input**
- User can open a dialog window with a canvas,
on which he can draw digitally the font


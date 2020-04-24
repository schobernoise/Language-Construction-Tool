import numpy as np
import random
import io
import os
import openpyxl as oxl
from openpyxl.styles import Font
import csv
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import *
from bs4 import BeautifulSoup
import requests
import docx
import pylatex as pyl
from pylatex.utils import italic

from controllers import utils, log


class data_controller():
    def __init__(self, vocab, conf):
        self.vocab = vocab
        self.conf = conf


    def load_excel(self, excel_file):
        wb = oxl.load_workbook(excel_file)
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
                for j, heading in enumerate(headings):
                    if row[j].value != None or heading == "related_image":
                        if heading != "related_image":
                            temp_word[heading] = row[j].value
                        else:
                            try:
                                image_dir = os.path.dirname(excel_file) + "/related_images/"
                                image = image_dir + str(i)+".jpg"
                                temp_word[heading] = utils.convertToBinaryData(image)
                            except:
                                pass
                import_dict.append(temp_word)
                
        self.vocab.import_words_from_file(import_dict)


    def load_csv(self, csv_file):
        
        import_dict = []
        headings = []
        with open(csv_file, "r", encoding="utf-8-sig") as csvfile:
            rows = csv.reader(csvfile, delimiter=';')
            for i, row in enumerate(rows):
                if i == 0:
                    for heading in row:
                        if heading != "":
                            headings.append(heading)
                else:
                    temp_word = {}
                    for j, heading in enumerate(headings):
                        if row[j] != "" or heading == "related_image":
                            if heading != "related_image":
                                temp_word[heading] = row[j]
                            else:
                                image_dir = os.path.dirname(csv_file) + "/related_images/"
                                image = image_dir + str(i)+".jpg"
                                temp_word[heading] = utils.convertToBinaryData(image)

                    import_dict.append(temp_word)
                    
        self.vocab.import_words_from_file(import_dict)
    
                   
    def text_extractor(self, filename, word_count=20, min_size=10, max_size=20 ):

        if filename[-3:] == "pdf":
        
            pdfFileObj = open(filename,'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            num_pages = pdfReader.numPages
            count = 0
            text = ""

            while count < num_pages:
                pageObj = pdfReader.getPage(count)
                count +=1
                text += pageObj.extractText()

            # Check if scanned File
            if text != "":
                text = text
            else:
                text = textract.process(fileurl, method='tesseract', language='de')
        
        elif filename[-3:] == "txt":
            f = open(filename, "r", encoding="utf-8-sig")
            text = f.read()
        
        elif filename[-4:] == "docx":
            document = docx.Document(filename)
            temp_text = []
            for para in document.paragraphs:
                temp_text.append(para.text)
            text = str(temp_text)

        tokens = word_tokenize(text)
        
        punctuations = ['(',')',';',':','[',']',',']
        stop_words = stopwords.words('german') 
        keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
        parametric_words = [w for w in keywords if len(w) > min_size and len(w) < max_size]

        fdist1 = FreqDist(parametric_words)
        fdist_counts = fdist1.most_common(word_count)

        final_wordlist = []

        for word in fdist_counts:
            temp_list = list(word)
            final_wordlist.append(temp_list[0])

        return(final_wordlist)


    def gen_words(self, letter_parts, word_count=30, min_size=2, max_size=6, hardness=4, foreigness=3):
        
        letters_list = np.random.randint(low = min_size, high = max_size, size = word_count)
        word = ""
        gen_words_list = []

        for letter_num in letters_list:
                prob = random.random()*100
                word = [" "] * letter_num

                for i in range(len(word)):
                    # FIRST CHAR CHOOSER
                    if i == 0:
                        cons_prob = self.translate(hardness, 1, 10, 1, 80)
                        vowels_prob = 100-cons_prob
                        spec_prob = (vowels_prob/100)*self.translate(foreigness, 1, 10, 1, 100)
                        vowel_prob = vowels_prob-spec_prob

                        if prob <=  cons_prob:
                            word[0] = random.choice(letter_parts["consonants"])

                        elif prob > cons_prob and prob < (cons_prob+vowel_prob):
                            word[0] = random.choice(letter_parts["vowels"])

                        elif prob >= (cons_prob+vowel_prob):
                            word[0] = random.choice(letter_parts["special_vowels"])
                    
                    else:
                        prob = random.random()*100  #Generate a new value for probability

                        # Char before WAS A KONS
                        for char in letter_parts["consonants"]:
                            if char == word[i-1]:

                                cons_prob = self.translate(hardness, 1, 10, 1, 60)
                                vowels_prob = 100-cons_prob
                                spec_prob = (vowels_prob/100)*self.translate(foreigness, 1, 10, 1, 100)
                                vowel_prob = vowels_prob-spec_prob

                                if prob <= cons_prob:
                                    word[i] = random.choice(letter_parts["consonants"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["consonants"])
                                    except:
                                        word[i] = random.choice(letter_parts["consonants"])

                                elif prob > cons_prob and prob < (cons_prob+vowel_prob):
                                    word[i] = random.choice(letter_parts["vowels"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["vowels"])
                                    except:
                                        word[i] = random.choice(letter_parts["vowels"])

                                elif prob >= (cons_prob+vowel_prob):
                                    word[i] = random.choice(letter_parts["special_vowels"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["special_vowels"])
                                    except:
                                        word[i] = random.choice(letter_parts["special_vowels"])

                            else: 
                                pass
                        
                        # Char before  WAS A VOWEL
                        for char in letter_parts["vowels"]:
                            if char == word[i-1]:

                                cons_prob = self.translate(hardness, 1, 10, 1, 85)
                                vowels_prob = 100-cons_prob
                                spec_prob = (vowels_prob/100)*self.translate(foreigness, 1, 10, 1, 100)
                                vowel_prob = vowels_prob-spec_prob

                                if prob <= cons_prob:
                                    word[i] = random.choice(letter_parts["consonants"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["consonants"])
                                    except:
                                        word[i] = random.choice(letter_parts["consonants"])

                                elif prob > cons_prob and prob < (cons_prob+vowel_prob):
                                    word[i] = random.choice(letter_parts["vowels"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["vowels"])
                                    except:
                                        word[i] = random.choice(letter_parts["vowels"])

                                elif prob >= (cons_prob+vowel_prob):
                                    word[i] = random.choice(letter_parts["special_vowels"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["special_vowels"])
                                    except:
                                        word[i] = random.choice(letter_parts["special_vowels"])
                            else:
                                pass


                        # Char before WAS A SPECIAL VOWEL
                        for char in letter_parts["special_vowels"]:
                            if char == word[i-1]:

                                cons_prob = self.translate(hardness, 1, 10, 1, 85)
                                vowels_prob = 100-cons_prob
                                spec_prob = (vowels_prob/100)*self.translate(foreigness, 1, 10, 1, 100)
                                vowel_prob = vowels_prob-spec_prob

                                if prob <= cons_prob:
                                    word[i] = random.choice(letter_parts["consonants"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["consonants"])
                                    except:
                                        word[i] = random.choice(letter_parts["consonants"])

                                elif prob > cons_prob and prob < (cons_prob+vowel_prob):
                                    word[i] = random.choice(letter_parts["vowels"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["vowels"])
                                    except:
                                        word[i] = random.choice(letter_parts["vowels"])

                                elif prob >= (cons_prob+vowel_prob):
                                    word[i] = random.choice(letter_parts["special_vowels"])
                                    try:
                                        while word[i] == word[i-1] and word[i] == word[i-2]:
                                            word[i] = random.choice(letter_parts["special_vowels"])
                                    except:
                                        word[i] = random.choice(letter_parts["special_vowels"])
                            else:
                                pass

                        

                word = "".join(word)
                gen_words_list.append(word)
                word = []

        gen_words_set = list(set(gen_words_list))
        return gen_words_set
    

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    
    def get_language_from_web(self, url="https://www.1000mostcommonwords.com/"):
        
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        links = {}

        if url == "https://www.1000mostcommonwords.com/":

            output = soup.find_all("a", attrs={"style" : "color: #0000ff;"})

            for link in output:
                links[link.find(text=True)] = link.get("href")
            
            return(links)
    

    def get_words_from_web(self, url, start_count=0, end_count=1000):
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        output = soup.find_all("tr")

        if "1000mostcommonwords" in url:

            words_list = []

            for row in output:
                words_dict = {}
                cell = row.find_all("td")
                words_dict["translation"]=cell[1].text 
                words_dict["english"]=cell[2].text

                words_list.append(words_dict)
            
        return(words_list[int(start_count):int(end_count)])
    

    def export_vocabulary_as_file(self, filename, vocabulary, formats, columns):
        for format_ in formats:
            if format_ == "CSV":
                if ".csv" not in filename:
                    output_name = str(filename) + ".csv"
                else:
                    output_name = filename

                with open(output_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(columns)
                    for word_ in vocabulary: 
                        temp_attr = []
                        for column in columns:
                            temp_attr.append(word_.attributes[column])  
                        writer.writerow(temp_attr)

            elif format_ == "XLSX":
                if ".xlsx" not in filename:
                    output_name = str(filename) + ".xlsx"
                else:
                    output_name = filename

                wb = oxl.Workbook()
                ws = wb.active
                ws.title = "vocabulary"
                ft = Font(bold=True)
                
                ws.append(columns)
                for word_ in vocabulary: 
                        temp_attr = []
                        for i, column in enumerate(columns): 
                            if column != "related_image":
                                temp_attr.append(word_.attributes[column])  
                        ws.append(temp_attr)

                for cell in ws["1"]:
                    cell.font = ft

                wb.save(filename = output_name)

            elif format_ == "TXT":
                if ".txt" not in filename:
                    output_name = str(filename) + ".txt"
                else:
                    output_name = filename
    

    def pretty_print_vocabulary(self, vocabulary, filename):

        geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
        doc = pyl.Document(geometry_options=geometry_options)

        doc.preamble.append(pyl.Command('title', 'Awesome Title'))
        doc.preamble.append(pyl.Command('author', 'Anonymous author'))
        doc.preamble.append(pyl.Command('date', pyl.NoEscape(r'\today')))
        doc.append(pyl.NoEscape(r'\maketitle'))

        for word_ in vocabulary:
            with doc.create(pyl.Section(word_.attributes["transliteration"])):
                doc.append(italic(word_.attributes["pos"]))
                doc.append(word_.attributes["translation"])
                
        print(filename)
        doc.generate_pdf(filepath=str(filename), compiler='pdflatex', clean_tex=True)

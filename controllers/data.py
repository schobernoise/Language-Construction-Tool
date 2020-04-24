import numpy as np
import random
import io
import openpyxl as oxl
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import *
from bs4 import BeautifulSoup
import requests

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
                for i, heading in enumerate(headings):
                    if row[i].value != None:
                        temp_word[heading] = row[i].value
                import_dict.append(temp_word)
                
        self.vocab.import_words_from_file(import_dict)


    def load_csv(self, csv_file):
        pass

    def pdf_extractor(self, filename, word_count=20, min_size=10, max_size=20 ):

        #open allows you to read the file.
        pdfFileObj = open(filename,'rb')
        #The pdfReader variable is a readable object that will be parsed.
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        #Discerning the number of pages will allow us to parse through all the pages.
        num_pages = pdfReader.numPages
        count = 0
        text = ""
        #The while loop will read each page.
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()
        #This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
        if text != "":
            text = text
        #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
        else:
            text = textract.process(fileurl, method='tesseract', language='de')
        #Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
        #Now, we will clean our text variable and return it as a list of keywords.

        #The word_tokenize() function will break our text phrases into individual words.
        tokens = word_tokenize(text)
        
        #We'll create a new list that contains punctuation we wish to clean.
        punctuations = ['(',')',';',':','[',']',',']
        #We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.
        stop_words = stopwords.words('german') 
        #We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
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




    



    






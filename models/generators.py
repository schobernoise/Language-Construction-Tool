import numpy as np

from lct import log
from lct.utils import utils

def gen_words(self, word_count=30, min_size=2, max_size=6):
        
        letters_list = np.random.randint(low = min_size, high = max_size, size = word_count)
        word = ""

        for letter_num in letters_list:
                prob = random.random()
                word = ["a"] * letter_num

                for i in range(len(word)):
                    # FIRST CHAR CHOOSER
                    if i == 0:
                        if prob <=  0.33:
                            word[0] = random.choice(self.kons)

                        elif prob > 0.33 and prob < 0.66:
                            word[0] = random.choice(self.vo)

                        elif prob >= 0.66:
                            word[0] = random.choice(self.vospec)
                    
                    else:
                        prob = random.random()  #Generate a new value for probability

                        # Char before WAS A KONS
                        for char in self.kons:
                            if char == word[i-1]:

                                if prob <= 0.03:
                                    word[i] = random.choice(self.vospec)

                                if prob > 0.03 and prob < 0.95:
                                    word[i] = random.choice(self.vospec)


                                if prob >= 0.95:
                                    word[i] = random.choice(self.kons)

                            else: 
                                pass

                        # Char before WAS A SPECIAL VOWEL
                        for char in self.vospec:
                            if char == word[i-1]:
                                # PROBABILITY FOR  SEPCIAL VOWEL: 1%
                                if prob <= 0.01:
                                    word[i] = random.choice(self.vo)

                                # PROBABILITY FOR KONS: 97.4%
                                if prob > 0.01 and prob < 0.975:
                                    word[i] = random.choice(self.kons)

                                # PROBABILITY FOR SPECIAL VOWEL: 2.5%
                                if prob >= 0.975:
                                    word[i] = random.choice(self.vospec)

                            else:
                                pass

                        # Char before  WAS A VOWEL
                        for char in self.vo:
                            if char == word[i-1]:
                                # PROBABILITY FOR  SEPCIAL VOWEL: 5%
                                if prob <= 0.05:
                                    word[i] = random.choice(self.vospec)
                                # PROBABILITY FOR KONS: 90%
                                if prob > 0.05 and prob < 0.95:
                                    word[i] = random.choice(self.kons)
                                # PROBABILITY FOR VOWEL: 5%
                                if prob >= 0.95:
                                    word[i] = random.choice(self.vo)
                            else:
                                pass

                word = "".join(word)
                self.gen_words_list.append(word)
                word = []

        return self.gen_words_list
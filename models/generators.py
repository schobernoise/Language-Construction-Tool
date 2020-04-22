import numpy as np
import random


def gen_words(letter_parts, word_count=30, min_size=2, max_size=6):
        
        letters_list = np.random.randint(low = min_size, high = max_size, size = word_count)
        word = ""
        gen_words_list = []

        for letter_num in letters_list:
                prob = random.random()
                word = [" "] * letter_num

                for i in range(len(word)):
                    # FIRST CHAR CHOOSER
                    if i == 0:
                        if prob <=  0.33:
                            word[0] = random.choice(letter_parts["consonants"])

                        elif prob > 0.33 and prob < 0.66:
                            word[0] = random.choice(letter_parts["vowels"])

                        elif prob >= 0.66:
                            word[0] = random.choice(letter_parts["special_vowels"])
                    
                    else:
                        prob = random.random()  #Generate a new value for probability

                        # Char before WAS A KONS
                        for char in letter_parts["consonants"]:
                            if char == word[i-1]:

                                if prob <= 0.03:
                                    word[i] = random.choice(letter_parts["consonants"])

                                elif prob > 0.03 and prob < 0.95:
                                    word[i] = random.choice(letter_parts["vowels"])

                                elif prob >= 0.95:
                                    word[i] = random.choice(letter_parts["special_vowels"])

                            else: 
                                pass

                        # Char before WAS A SPECIAL VOWEL
                        for char in letter_parts["special_vowels"]:
                            if char == word[i-1]:

                                if prob <= 0.01:
                                    word[i] = random.choice(letter_parts["vowels"])

                                elif prob > 0.01 and prob < 0.975:
                                    word[i] = random.choice(letter_parts["consonants"])

                                elif prob >= 0.975:
                                    word[i] = random.choice(letter_parts["special_vowels"])
                            else:
                                pass

                        # Char before  WAS A VOWEL
                        for char in letter_parts["vowels"]:
                            if char == word[i-1]:

                                if prob <= 0.05:
                                    word[i] = random.choice(letter_parts["special_vowels"])

                                elif prob > 0.05 and prob < 0.95:
                                    word[i] = random.choice(letter_parts["consonants"])

                                elif prob >= 0.95:
                                    word[i] = random.choice(letter_parts["vowels"])
                            else:
                                pass

                word = "".join(word)
                gen_words_list.append(word)
                word = []

        gen_words_set = list(set(gen_words_list))
        return gen_words_set


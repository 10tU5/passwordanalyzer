"""
Created on Wed Feb  10 11:15:33 2021

@author: Aquif R Mir
"""

"""
--RULE-BASED COMPONENT
paswordstrength module can be used to get a password strength score of a password-string. 
It is based on various rules which are similar to those found in Wolfram Alpha.
"""

import os
# from argparse import ArgumentParser
# import getpass
import string

# Only load it once.
with open(os.path.join('./english'), 'r') as f:
    words = set(f.read().split('\n'))

class passwordstrength:
    # def __init__(self, password, verbose=False):
    def __init__(self, password):
        self.words = words  
        
        self.password = password
        self.password_length = len(password)
        self.strength_flags = {
            "length": 0,
            "upper_case": 0,
            "lower_case": 0,
            "digits": 0,
            "special_chars": 0,
            "middle_num_symbol": 0,
            "extra": 0,
            "letters_only": 2,
            "numbers_only": 2,
            "repeating_chars": 2,
            "consecutive_upper_case": 2,
            "consecutive_lower_case": 2,
            "consecutive_digits": 2,
            "sequential_letters": 2,
            "sequential_nums": 2,
            "dictionary_word": 2
        }
        
        # self.verbose = verbose
        # if verbose:
        #     print(("{:>45s}{:>13s}".format("Count", "Value")))
        #     print(('='*80))
            
        # self.length_score = self.__length_score()
        
        #Calculating the score
        self.score = sum((
            self.__length_score(),
            self.__lower_upper_case_score(),
            self.__digits_score(),
            self.__special_score(),
            self.__middle_score(),
            self.__letters_only_score(),
            self.__numbers_only_score(),
            self.__repeating_chars_score(),
            self.__consecutive_case_score(),
            self.__sequential_letters_score(),
            self.__sequential_numbers_score(),
            self.__dictionary_words_score(),
            self.__extra_score()
            ))

        # if verbose:
        #     print(('-'*80))
        #     print(("{:>45s}{}{:=+4d}".format("Total", ' '*8, self.score)))
    
    # def __table_print(self, title, count, value):
    #     if self.verbose:
    #         title = title.capitalize()
    #         count = str(count)
            
    #         print("{title:40s}{count:13s}{value:=+4d}".format(**locals()))
            
    def __chars_of_type(self, chartype):
        chartype_count = 0
        for char in self.password:
            if char in chartype:
                chartype_count += 1
        
        return chartype_count
    
    def __length_score(self):
        # self.__table_print('length', self.password_length, self.password_length * 4)
        if self.password_length > 8:
            self.strength_flags["length"] = 3
        elif self.password_length == 8:
            self.strength_flags["length"] = 2
        
        return self.password_length * 4 #The way WA works.
    
    def __lower_upper_case_score(self):
        #This will return the number of upper and lower case characters,
        #if at least one of each is available.
        n_upper = self.__chars_of_type(string.ascii_uppercase)
        n_lower = self.__chars_of_type(string.ascii_lowercase)
        
        # upper_score = 0 if not n_upper else (self.password_length - n_upper)*2
        # lower_score = 0 if not n_lower else (self.password_length - n_lower)*2

        if not n_upper:
            upper_score = 0
        else:
            upper_score = (self.password_length - n_upper)*2

            if n_upper == 1:
                self.strength_flags["upper_case"] = 2
            else:
                self.strength_flags["upper_case"] = 3

        if not n_lower:
            lower_score = 0
        else:
            lower_score = (self.password_length - n_lower)*2

            if n_lower == 1:
                self.strength_flags["lower_case"] = 2
            else:
                self.strength_flags["lower_case"] = 3
            
        # self.__table_print('upper case letters', n_upper, upper_score)
        # self.__table_print('lower case letters', n_lower, lower_score)
        
        if lower_score and upper_score:
            return lower_score + upper_score

        return 0
    
    def __digits_score(self):
        digit_count = self.__chars_of_type(string.digits)
        
        if digit_count == 1:
            self.strength_flags["digits"] = 2
        elif digit_count > 1:
            self.strength_flags["digits"] = 3
        
        # self.__table_print('numbers', digit_count, digit_count * 4)
        
        return digit_count * 4 #The way WA works.
    
    def __special_score(self):
        special_char_count = self.__chars_of_type(string.punctuation)
        
        if special_char_count == 1:
            self.strength_flags["special_chars"] = 2
        elif special_char_count > 1:
            self.strength_flags["special_chars"] = 3
        
        # self.__table_print('special characters', special_char_count,
        #                    special_char_count * 6)
        
        return special_char_count * 6 #The way WA works.

    def __middle_score(self):
        #WA doesn't count special characters in this score (which probably
        #is a mistake), but we will.
        middle_chars_count = 0
        
        middle_chars = set(string.punctuation + string.digits)
        
        for char in self.password[1:-1]:
            if char in middle_chars:
                middle_chars_count += 1
            
        if middle_chars_count == 1:
            self.strength_flags["middle_num_symbol"] = 2
        elif middle_chars_count >1:
            self.strength_flags["middle_num_symbol"] = 3
        
        # self.__table_print('middle numbers or special characters',
        #                    middle_chars_count, middle_chars_count * 2)
        
        return middle_chars_count * 2 #The way WA works
        
    
    def __letters_only_score(self):
        letter_count = self.__chars_of_type(string.ascii_lowercase + string.ascii_uppercase)
        
        if self.password_length == letter_count:
            
            self.strength_flags["letters_only"] = 1
            # self.__table_print('letters only', 'yes', -self.password_length)
            
            #If the password is all letters, return the negative
            #of the password length. The way WA works.
            return -self.password_length

        # self.__table_print('letters only', 'no', 0)
        
        #If the password contains something else than letters,
        #don't affect the score.
        return 0
    
    def __numbers_only_score(self):
        digit_count = self.__chars_of_type(string.digits)
        
        if self.password_length == digit_count:
            
            self.strength_flags["numbers_only"] = 1
            # self.__table_print('numbers only', 'yes', -self.password_length)
            
            #If the password is all numbers, return the negative
            #form of the password length. The way WA works.
            return -self.password_length

        # self.__table_print('numbers only', 'no', 0)
        
        #If the password contains something else than numbers,
        #don't affect the score.
        return 0
    
    def __repeating_chars_score(self):
        repeating_char_count = self.password_length - len(set(self.password))
        
        if repeating_char_count:
            self.strength_flags["repeating_chars"] = 1
        
        # self.__table_print('repeating characters', repeating_char_count,
        #                    -repeating_char_count)
        
        return -repeating_char_count #The way WA works
    
    def __consecutive_case_score(self):
        char_types = {
            string.ascii_lowercase: 0,
            string.ascii_uppercase: 0,
            string.digits   : 0,
            }

        for c1, c2 in zip(self.password, self.password[1:]):
            #zips match the length of the shorter by default
            
            for char_type in char_types:
                if c1 in char_type and c2 in char_type:
                    char_types[char_type] += 1
        
        if char_types[string.ascii_uppercase]:
            self.strength_flags["consecutive_upper_case"] = 1
        
        if char_types[string.ascii_lowercase]:
            self.strength_flags["consecutive_lower_case"] = 1
            
        if char_types[string.digits]:
            self.strength_flags["consecutive_digits"] = 1
            
        
        # self.__table_print('consecutive upper-case letters',
        #                    char_types[string.ascii_uppercase],
        #                    -2*char_types[string.ascii_uppercase])
        
        # self.__table_print('consecutive lower-case letters',
        #                    char_types[string.ascii_lowercase],
        #                    -2*char_types[string.ascii_lowercase])
        
        # self.__table_print('consecutive numbers',
        #                    char_types[string.digits],
        #                    -2*char_types[string.digits])
        
        return -2*sum(char_types.values()) #The way WA works

    def __sequential_numbers_score(self):
        sequential_number_count = 0
        
        for i in range(1000):
            if str(i) + str(i + 1) in self.password:
                sequential_number_count += 2
                
        if sequential_number_count:
            self.strength_flags["sequential_nums"] = 1
            
        # self.__table_print('sequential numbers', sequential_number_count,
        #                    -sequential_number_count*2)

        return -sequential_number_count * 2

    def __sequential_letters_score(self):
        password = self.password.lower()
        
        sequential_letter_count = 0

        seeing = False
        for c1, c2 in zip(password, password[1:]):
            #zips match the length of the shorter by default
            if ord(c1)+1 == ord(c2) and c1 in string.ascii_lowercase[:-1]:
                sequential_letter_count += 1

                if not seeing:
                    #until now, we weren't in a pocket of sequential letters
                    sequential_letter_count += 1
                    seeing = True
            else:
                #we've seen a whole pocket, and counted everything
                seeing = False
        
        sequential_letter_count -= 2 #The way WA works

        if sequential_letter_count > 0:
            # self.__table_print('sequential letters',
            #                    sequential_letter_count,
            #                    sequential_letter_count * -2)
            self.strength_flags["sequential_letters"] = 1
            return sequential_letter_count * -2 #The way WA works

        # self.__table_print('sequential letters', 0, 0)
        
        return 0

    def __substrings(self, word):
        #generate all substrings of length at least 3
        for i in range(len(word)):
            for j in range(i+3, len(word)+1):
                yield word[i:j]

    def __dictionary_words_score(self):
        password_substrings = self.__substrings(self.password)
        
        if self.words.intersection(password_substrings):
            # self.__table_print('contains dictionary word', 'yes', -20)
            self.strength_flags["dictionary_word"] = 1
            return -20

        # self.__table_print('contains dictionary word', 'no', 0)
        return 0

    def __extra_score(self):
        if self.password_length < 8:
            # self.__table_print('extra criteria', 'no', 0)
            return 0

        upper = False
        lower = False
        special = False
        number = False

        for char in self.password:
            if char in string.ascii_uppercase:
               upper = True
            elif char in string.ascii_lowercase:
                lower = True
            elif char in string.punctuation:
                special = True
            elif char in string.digits:
                number = True

        if upper and lower and (special or number):
            # self.__table_print('extra criteria', 'yes', 8)
            if special and number:
                self.strength_flags["extra"] = 3
            else:
                self.strength_flags["extra"] = 2
            
            return 8

        return 0
    
    def get_score(self):
        return self.score
    
    def get_readable_score(self):
        if self.score < 0:
            return 'Very weak'
        elif self.score < 30:
            return 'Weak'
        elif self.score < 60:
            return 'OK'
        elif self.score < 80:
            return 'Strong'

        return 'Very strong'
    
    def get_results(self):
        results = {
            "length_score" : self.__length_score(),
            "lower_upper_case_score" : self.__lower_upper_case_score(),
            "digits_score" : self.__digits_score(),
            "special_score" : self.__special_score(),
            "middle_score" : self.__middle_score(),
            "letters_only_score" : self.__letters_only_score(),
            "numbers_only_score" : self.__numbers_only_score(),
            "repeating_chars_score" : self.__repeating_chars_score(),
            "consecutive_case_score" : self.__consecutive_case_score(),
            "sequential_letters_score" : self.__sequential_letters_score(),
            "sequential_numbers_score" : self.__sequential_numbers_score(),
            "dictionary_words_score" : self.__dictionary_words_score(),
            "extra_score" : self.__extra_score()
            }
        return results
    
    def get_strength_flags(self):
        return self.strength_flags

# For Unit Testing of passwordstrength module.

# def main():
#     ap = ArgumentParser(description='Checks the strength of a password.')
#     ap.add_argument('-r', '--readable', action='store_true',
#                     help="Outputs the english score.")
#     ap.add_argument('-v', '--verbose', action='store_true',
#                     help='Outputs a scoring table.')
#     args = ap.parse_args()
    
#     strength = passwordstrength(getpass.getpass("Password: "),
#                                 verbose=args.verbose)
#     if args.readable:
#         print("Score:", strength.get_score())
#         print(strength.get_readable_score())
#     else:
#         print("Score:", strength.get_score())

# if __name__ == "__main__":
#     main()
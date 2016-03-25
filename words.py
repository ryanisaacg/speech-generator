import re
"""
get_word_list(text : String) -> [String]
Creates a list of all the words found in the text, in order, in lowercase
Splits at any space character
"""
def get_word_list(text):
    all_words = text.split(" ");
    #Matches only non-alphabetic characters
    regex = re.compile('[^a-zA-Z]')
    for i in range(0, len(all_words)):
        #Get the word in lower case, with all non-alphabetic characters removed
        all_words[i] = regex.sub('', all_words[i]).lower()
    return all_words

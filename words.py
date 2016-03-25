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
LOOK_AHEAD_AMT = 10
"""
get_word_map(word_list : [String]) -> {String : LOOK_AHEAD_AMT[{String : Int}]}
Creates a map of words that are often found in the next ten words after a specific word
"""
def get_word_map(word_list):
    word_map = {} #{String :{String : LOOK_AHEAD_AMT[{String : Int}]}
    #Increment a key/value pair in the word map
    def add_to_entry(key_word, index, value_word):
        if value_word in word_map[key_word][index]:
            word_map[key_word][index][value_word] += 1
        else:
            word_map[key_word][index][value_word] = 1
    for i in range(0, len(word_list)):
        word = word_list[i]
        if not word in word_map:
            word_map[word] = [{} for x in range(0, LOOK_AHEAD_AMT)]
        j = i + 1
        while j < i + 10 and j < len(word_list):
            add_to_entry(word, j - i - 1, word_list[j])
            j += 1
    return word_map
with open('story.txt') as text:
    data = text.read()
print(get_word_map(get_word_list(data)));

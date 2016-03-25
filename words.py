import re
from random import random
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
"""
get_word_probabilities(word : String, offset : Int, word_map : {String : [{String : Int}]}) -> {String : Float}
word is the prompt for the generator
offset is the number of words after the generated word should be
word_map is the output of get_word_map
It returns the probabilities for every possible subsequent word, with a total of 1 / offset
"""
def get_word_probabilities(word, offset, word_map):
    data = word_map[word][offset - 1] #get only the relevant data
    total = 0 #The total number of all of the counts of all of the occurences
    for key in data.keys():
        total += data[key]
    scaled = {}
    for key in data.keys():
        scaled[key] = data[key] / float(total) / offset
    return scaled
"""
get_next_word(context : [String], word_map : {String : [{String : Int}]}) -> String
context are all the previous words in the chain
word_map is the output for get_word_map
returns the next word as chosen by a weighted random number generator
"""
def get_next_word(context, word_map):
    start = max(len(context) - LOOK_AHEAD_AMT, 0) #Find the starting point for the actual context we'll use
    probabilities = {}
    total = 0
    #Collect the word probabilities as given by the get_word_probabilities function
    for word_index in range(start, len(context)):
        new_probabilities = get_word_probabilities(context[word_index], word_index - start, word_map)
        for key in new_probabilities.keys():
            if key in probabilities:
                probabilities[key] += new_probabilities[key]
                total += new_probabilities[key]
            else:
                probabilities[key] = new_probabilities[key]
                total += new_probabilities[key]
    #Create an array of key-value pairs where the key is the word and the value is the minimum number threshold to produce that word
    running_total = 0
    probability_array = []
    for key in probabilities:
        probabilities[key] /= total #Guarantee that all entries will be normalized and the total will be 1
        probability_array.append([probabilities[key] + running_total, key])
        running_total += probabilities[key]
    #Generate a random number to use to pick
    number = random()
    index = 0
    while probability_array[index][0] < number and index < len(probability_array):
        index += 1
    return probability_array[index][1]
with open('input.txt') as text:
    data = text.read()
word_list = get_word_list(data)
word_map = get_word_map(word_list)
NUMBER_GENERATE = 30
context = word_list[0:10:]
print("Generating using the initial string of: " + " ".join(context))
for i in range(NUMBER_GENERATE):
    next = get_next_word(context, word_map)
    context.append(next)
print("Generated: " +  " ".join(context))

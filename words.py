import re
def get_word_list(text):
    all_words = text.split(" ");
    regex = re.compile('[^a-zA-Z]')
    for i in range(0, len(all_words)):
        all_words[i] = regex.sub('', all_words[i]).lower()
    return all_words

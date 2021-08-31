import pandas as pd
from nltk.stem import PorterStemmer


def read_wordlist_file(filename):
    """
    Reads the words' list file and returns its insides as a list
    :param filename: The name of the words file
    :return: A list contains the words from the file
    """
    words = open(filename)
    word_file = []
    for word in words.readlines():
        word_file.append(word[:-1])
    words.close()
    return word_file


def book_stemming(words_list):
    """
    Gets a list and returns the same list stemmed
    :param words_list: A list of words
    :return: The words list, with every word in it stemmed
    """
    porter = PorterStemmer()
    for i in range(len(words_list)):
        words_list[i] = porter.stem(words_list[i])
    return words_list


def remake_dicts(filename):
    """
    A function that gets a file name of our songs dataframe, and updates the
    profanities dictionary of every song in it, using stemming
    :param filename: The name of the file we want to update its songs'
    profanities dictionary
    :return: Nothing. Re-writes the file
    """
    df = pd.read_json(filename, orient='table')
    profanities = read_wordlist_file('bad-words.txt')
    lst = []
    for row in df.iterrows():
        used_swears = {}
        lyrics = row[1]['Lyrics']
        for ind in range(len(lyrics)):
            lyrics[ind] = lyrics[ind].replace('-', '').lower()
        lyrics = book_stemming(lyrics)
        for word in lyrics:
            if word in profanities:
                if word in used_swears:
                    used_swears[word] += 1
                else:
                    used_swears[word] = 1
        lst.append(used_swears)
    df['Profanities'] = lst
    df.to_json(filename, orient='table', indent=4)


if __name__ == '__main__':
    for i in range(1, 73):
        print("working on file" + str(i))
        remake_dicts('songs_dt_part_' +  str(i) + '.json')
    for i in range(1, 31):
        print("working on file" + str(i))
        remake_dicts('songs_dt_w_gen_ethn_part_' + str(i) + '.json')
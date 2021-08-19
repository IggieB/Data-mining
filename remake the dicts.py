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


def write_output_file(results, output_filename):
    results = '\n'.join(results)
    file = open(output_filename, 'w')
    file.writelines(results)
    file.close()


def book_stemming(words_list):
    porter = PorterStemmer()
    for i in range(len(words_list)):
        words_list[i] = porter.stem(words_list[i])
    return words_list


def remake_dicts(filename):
    df = pd.read_json(filename, orient='table')
    profanities = read_wordlist_file('bad-words.txt')
    for row in df.iterrows():
        used_swears = {}
        lyrics = row[1]['Lyrics']
        for ind in range(len(lyrics)):
            lyrics[ind] = lyrics.replace('-', '')
        lyrics = book_stemming(lyrics)
        for word in lyrics:
            if word in profanities:
                if word not in used_swears:
                    used_swears[word] = 1
                else:
                    used_swears[word] += 1
        df.loc[row[0], 'Profanities'] = used_swears
    df.to_json(filename, orient='table', indent=4)


if __name__ == '__main__':
    all_profanities = read_wordlist_file('bad-words.txt')
    lst = book_stemming(all_profanities)
    print(len(lst))
    new_lst = []
    for word in lst:
        if word not in new_lst:
            new_lst.append(word)
    write_output_file(new_lst, 'bad-words2.txt')
    print(len(new_lst))
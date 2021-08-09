import pandas as pd


def read_wordlist_file(filename):
    """
    Reads the words' list file and returns its insides as a list
    :param filename: The name of the words file
    :return: A list contains the words from the file
    """
    words = open(filename)
    lines = words.readlines()
    words.close()
    for ind in range(len(lines)):
        if '"Date":' in lines[ind]:
            if 'NaT' in lines[ind]:
                lines[ind] = lines[ind].replace('NaT', 'nan')
    new_file_contents = "".join(lines)
    my_file = open('songs_dt2.json', "w")
    my_file.write(new_file_contents)
    my_file.close()


def read_jas(filename):
    df = pd.read_json(filename, orient='table')
    print(df['Date'])


# read_wordlist_file('songs_dt2.json')
read_jas('songs_dt5.json')

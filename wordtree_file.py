import wordtree
import pandas as pd
########## WARNING! #################
# You need to have Graphviz installed on your machine for this to work!
# install at: https://www.graphviz.org/download/


FULL_DB_FILES = ["songs_dt_part_" + str(i) + ".json" for i in range(1, 73)]
ARTISTS_DB_FILES = ["songs_dt_w_gen_ethn_part_" + str(i) + ".json" for i in
                    range(1, 31)]
COLUMNS = ["Song", "Artist", "Gender", "Ethnicity", "Album", "Date", "URL",
           "Profanities", "Lyrics"]


def load_json_data(json_files):
    """
    this function takes a list of json files and converts them into one
    dataframe
    :param json_files: The DB json files
    :return: a dataframe
    """
    full_data = pd.DataFrame()
    for file in json_files:
        single_file_df = pd.read_json(file, orient='table')
        full_data = full_data.append(single_file_df)
    return full_data

def unite_lyrics(data_df):
    """
    this function gets a dataframe converts the lyrics column (was scraped
    as a list of strings) into one long string for the clustering
    :param data_df: the data dataframe
    :return: a new dataframe with the same data but the lyrics are a one
    long string
    """
    united_lyrics_df = pd.DataFrame()
    for index, row in data_df.iterrows():
        song_details = [row['Song'], row['Artist'], row['Gender'],
                        row['Ethnicity'], row['Album'], row['Date'],
                        row['URL'], row['Profanities'],
                        " ".join(row['Lyrics'])]
        united_lyrics_df = united_lyrics_df.append(pd.DataFrame(columns=COLUMNS,
                                                  data=[song_details]))
    return united_lyrics_df


def create_wordtree(lyrics, chosen_word):
    """
    this function creates a word tree that follow the most popular leading
    words to a certain keyword, and than the most popular words stemming
    from that keyword.
    :param lyrics: a list that has a sample of the songs lyrics
    :param chosen_word: the word that will be the core of the tree
    :return: nothing, creates a photo file with the results.
    """
    g = wordtree.search_and_draw(corpus=lyrics, keyword=chosen_word)
    # creates 2 files: onr is keyword.gv (irrelevant) the other is
    # keyword.gv.png - a normal photo file that one can open.
    g.render()

if __name__ == '__main__':
    ############ Loading the data ##########3
    full_data_df = load_json_data(ARTISTS_DB_FILES)
    full_data_df_frac = unite_lyrics(full_data_df.sample(n=500))
    songs_lyrics = list(full_data_df_frac["Lyrics"])
    # asking for user input to choose a keyword to look for
    chosen_word = str(input("Please choose a word to look for: "))
    # creating the wordtree
    create_wordtree(songs_lyrics, chosen_word)
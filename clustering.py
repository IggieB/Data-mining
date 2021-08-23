import pandas as pd
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


TEST_FILE = ["clustering_test_file.json"]
DATA_FILES = ["songs_dt_part_" + str(i) + ".json" for i in range(1, 51)]
COLUMNS = ["Song", "Artist", "Gender", "Ethnicity", "Album", "Date", "URL",
           "Profanities", "Lyrics"]


def remove_stopwords(words_list):  # c, d
    """
    A function that removes stop words from a list of words.
    :param words_list: a list of strings, representing words.
    :return: a list of strings, without the strings that represent stop words.
    """
    stop_words = stopwords.words('english')
    words_without_stops = []
    for word in words_list:
        word_parts = word.split("'")
        for part in word_parts:
            if part == '':
                continue
            elif part not in stop_words:
                words_without_stops.append(part)
    return words_without_stops


def load_json_data(files):
    full_data = pd.DataFrame()
    for file in files:
        single_file_df = pd.read_json(file, orient='table')
        for index, row in single_file_df.iterrows():
            no_stop_lyrics = remove_stopwords(row['Lyrics'])
            song_details = [row['Song'], row['Artist'], row['Gender'],
                            row['Ethnicity'], row['Album'], row['Date'],
                            row['URL'], row['Profanities'], no_stop_lyrics]
            full_data = full_data.append(pd.DataFrame(columns=COLUMNS,
                                                    data=[song_details]))
    return full_data


def create_clusters():
    pass


if __name__ == '__main__':
    documents = load_json_data(TEST_FILE)
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

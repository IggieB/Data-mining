import pandas as pd
from bs4 import BeautifulSoup
import requests
NIKUDS = ['.', ',', ':', ';', '!', '?', ' &']
COLUMNS = ["Song", "Artist", "Gender", "Ethnicity", "Album", "Date", "URL",
           "Profanities", "Lyrics"]
DATA_FILES = ["songs_dt_part_" + str(i) + ".json" for i in range(1, 73)]
# dict with all the relevant wiki tag page links
WIKI_CATEGORIES = {
    "African-American Female": [
        "https://en.wikipedia.org/wiki/Category:African-American_female_rappers"],
    "Puerto Rican Female": [
        "https://en.wikipedia.org/wiki/Category:Puerto_Rican_female_rappers"],
    "Puerto Rican Male": ["https://en.wikipedia.org/wiki/Category"
                          ":Puerto_Rican_rappers"],
    "Native American Male": [
        "https://en.wikipedia.org/wiki/Category:Native_American_rappers"],
    "American-Filipino Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Filipino_descent"],
    "American-East Asian Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_East_Asian_descent"],
    "American-Asian Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Asian_descent"],
    "American-Mexican Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Mexican_descent"],
    "American-Dominican Republic Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Dominican_Republic_descent"],
    "American-Panamanian Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Panamanian_descent"],
    "American-Hispanic and Latino Unknown": [
        "https://en.wikipedia.org/wiki/Category:Hispanic_and_Latino_American_rappers"],
    "American-Jamaican Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Jamaican_descent"],
    "American-Haitian Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Haitian_descent"],
    "American-Caribbean Unknown": [
        "https://en.wikipedia.org/wiki/Category:American_rappers_of_Caribbean_descent"],
    "African-American Male": [
        "https://en.wikipedia.org/w/index.php?title=Category:African"
        "-American_male_rappers&pageuntil=Coleman%2C+Charles%0ACharles+Coleman+%28music+producer%29#mw-pages",
        "https://en.wikipedia.org/w/index.php?title=Category:African"
        "-American_male_rappers&pagefrom=Coleman%2C+Charles%0ACharles+Coleman+%28music+producer%29#mw-pages",
        "https://en.wikipedia.org/w/index.php?title=Category:African"
        "-American_male_rappers&pagefrom=Harrell%2C+Andre%0AAndre+Harrell#mw-pages",
        "https://en.wikipedia.org/w/index.php?title=Category:African"
        "-American_male_rappers&pagefrom=Logic%0ALogic+%28rapper%29#mw-pages",
        "https://en.wikipedia.org/w/index.php?title=Category:African"
        "-American_male_rappers&pagefrom=Razah%2C+Hell%0AHell+Razah#mw-pages",
        "https://en.wikipedia.org/w/index.php?title=Category:African"
        "-American_male_rappers&pagefrom=Tjay%2C+Lil%0ALil+Tjay#mw-pages"],
    "Moroccan Unknown": ["https://en.wikipedia.org/wiki/Category"
                         ":Moroccan_rappers"],
    "Palestinian Unknown": [
        "https://en.wikipedia.org/wiki/Category:Palestinian_rappers"],
    "Australian Female": ["https://en.wikipedia.org/wiki/Category"
                          ":Australian_female_rappers"],
    "Black British Female": [
        "https://en.wikipedia.org/wiki/Category:Black_British_female_rappers"],
    "English Female": ["https://en.wikipedia.org/wiki/Category"
                       ":English_female_rappers"],
    "British Female": ["https://en.wikipedia.org/wiki/Category"
                       ":British_female_rappers"],
    "Canadian Female": ["https://en.wikipedia.org/wiki/Category"
                        ":Canadian_female_rappers"],
    "German Female": ["https://en.wikipedia.org/wiki/Category"
                      ":German_female_rappers"],
    "South Korean Female": [
        "https://en.wikipedia.org/wiki/Category:South_Korean_female_rappers"],
    "Australian Male": ["https://en.wikipedia.org/wiki/Category"
                        ":Australian_male_rappers"],
    "English Male": ["https://en.wikipedia.org/wiki/Category"
                     ":English_male_rappers"],
    "Canadian Male": ["https://en.wikipedia.org/wiki/Category"
                      ":Canadian_male_rappers"],
    "Mexican Male": ["https://en.wikipedia.org/wiki/Category"
                     ":Mexican_male_rappers"],
    "Nigerian Male": ["https://en.wikipedia.org/wiki/Category"
                      ":Nigerian_male_rappers"],
    "South Korean Male": ["https://en.wikipedia.org/wiki/Category"
                          ":South_Korean_male_rappers"],
    "Spanish Male": ["https://en.wikipedia.org/wiki/Category"
                     ":Spanish_male_rappers"],
    "French Unknown": ["https://en.wikipedia.org/wiki/Category"
                       ":French_rappers"],
    "South African Unknown": [
        "https://en.wikipedia.org/wiki/Category:South_African_rappers"],
    }


def get_wiki_category_names(link_list):
    """
    this function gets one wiki category and finds all the artist that fall
    into that category (according to wiki)
    :param link_list: all pages related to one wiki category
    :return: list of all artists in that category
    """
    artist_list = []
    for link in link_list:
        # getting the data from the web page
        new_link = link
        html = requests.get(new_link).text
        soup = BeautifulSoup(html, 'html.parser')
        artists_div = soup.find(id="mw-pages").findAll("li")
        for artist in artists_div:
            # sometimes theres is a suffix like (rapper) - this removes it
            if artist.text.endswith(")"):
                artist_name = artist.text.split(" ")
                artist_name = " ".join(string for string in
                                       artist_name[:-1])
                # upper because all the names in the jsons are uppercase
                artist_list.append(artist_name.upper())
            else:
                artist_list.append(artist.text.upper())
    return artist_list


def create_artist_gender_ethnicity_dict():
    """
    creating the full dictionary, keys are gender and ethnicity categories
    values are lists of all artist in each category
    :return: a dictionary with gender and ethnicity categories as keys and a
    list of relevant artists in each value
    """
    artist_gender_ethnicity_dict = {}
    for key, val in WIKI_CATEGORIES.items():
        artist_gender_ethnicity_dict[key] = get_wiki_category_names(val)
    return artist_gender_ethnicity_dict


def add_ethnicity_field(files):
    """
    this function goes over al the previously collected songs_dt files and
    add an "Ethnicity" field in each row (was not collected in the beginning)
    :param files: list of all the songs_dt files (5 total)
    :return: nothing - saves the new data to the original files
    """
    for file in files:
        file_df = pd.read_json(file, orient='table')
        file_df.insert(3, "Ethnicity","Unknown")
        file_df.reset_index(drop=True, inplace=True)
        file_df.to_json(file, orient='table', indent=4)


def insert_gender_ethnicity_to_data(files):
    """
    this function executes the "injection" of gender and ethnicity data in
    the original songs_dt files if found (checks for each artist).
    :param files: list of all the songs_dt files (5 total)
    :return: nothing - saves the new data to the original files
    """
    # generating the full gender and ethnicity data dict from wiki
    artist_wiki_dict = create_artist_gender_ethnicity_dict()
    for file in files:
        file_df = pd.read_json(file, orient='table')
        for index, row in file_df.iterrows():
            # changing the irrelevant values in this field fron the initial
            # data collection
            file_df.loc[index, 'Gender'] = "Unknown"
            for key, val in artist_wiki_dict.items():
                # checking if there is gender and ethnicity data for each
                # artist. if so it will be inserted to the dataframe
                if row['Artist'] in val:
                    wiki_tags = key.split()
                    file_df.loc[index, 'Gender'] = wiki_tags[-1]
                    file_df.loc[index, 'Ethnicity'] = " ".join(wiki_tags[:-1])
        # saving the new data into the original json files
        file_df.reset_index(drop=True, inplace=True)
        file_df.to_json(file, orient='table', indent=4)


def create_data_only_with_gen_and_ethnicity(files):
    """
    this function create a new json file that contain only the data of
    artists who has gender and ethnicity details. meant to allow us more
    analysis when needed.
    :param files: list of all the songs_dt files (5 total)
    :return: nothing - saves a new data file
    """
    songs_dt = pd.DataFrame(columns=COLUMNS)
    for file in files:
        file_df = pd.read_json(file, orient='table')
        for index, row in file_df.iterrows():
            # checking for each artist if there is gender or ethnicity data.
            # if so adds the artist row to a new dataframe
            if row['Gender'] != "Unknown" or row['Ethnicity'] != "Unknown":
                if row["Lyrics"] not in songs_dt.values:
                    song_details = [row['Song'], row['Artist'], row['Gender'],
                                    row['Ethnicity'], row['Album'], row['Date'],
                                    row['URL'], row['Profanities'], row["Lyrics"]]
                    print(song_details)
                    songs_dt = songs_dt.append(pd.DataFrame(columns=COLUMNS,
                                                            data=[song_details]))
    # saving the new dataframe to a new file
    songs_dt.reset_index(drop=True, inplace=True)
    songs_dt.to_json('artists_with_gender_or_ethnicity.json',
                     orient='table', indent=4)


if __name__ == "__main__":
    create_data_only_with_gen_and_ethnicity(DATA_FILES)

import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
NIKUDS = ['.', ',', ':', ';', '!', '?', ' &']
WIKI_CATEGORIES = {
    "African-American female": ["https://en.wikipedia.org/wiki/Category:African-American_female_rappers"],
    "Puerto Rican female": ["https://en.wikipedia.org/wiki/Category:Puerto_Rican_female_rappers"],
    "Puerto Rican male": ["https://en.wikipedia.org/wiki/Category:Puerto_Rican_rappers"],
    "Native American male": ["https://en.wikipedia.org/wiki/Category:Native_American_rappers"],
    "American-Filipino unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Filipino_descent"],
    "American-East Asian unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_East_Asian_descent"],
    "American-Asian unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Asian_descent"],
    "American-Mexican unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Mexican_descent"],
    "American-Dominican Republic unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Dominican_Republic_descent"],
    "American-Panamanian unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Panamanian_descent"],
    "American-Hispanic and Latino unknown": ["https://en.wikipedia.org/wiki/Category:Hispanic_and_Latino_American_rappers"],
    "American-Jamaican unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Jamaican_descent"],
    "American-Haitian unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Haitian_descent"],
    "American-Caribbean unknown": ["https://en.wikipedia.org/wiki/Category:American_rappers_of_Caribbean_descent"],
    "African-American male": [
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
    "Moroccan unknown": ["https://en.wikipedia.org/wiki/Category:Moroccan_rappers"],
    "Palestinian unknown": ["https://en.wikipedia.org/wiki/Category:Palestinian_rappers"],
    "Australian female": ["https://en.wikipedia.org/wiki/Category:Australian_female_rappers"],
    "Black British female": ["https://en.wikipedia.org/wiki/Category:Black_British_female_rappers"],
    "English female": ["https://en.wikipedia.org/wiki/Category:English_female_rappers"],
    "British female": ["https://en.wikipedia.org/wiki/Category:British_female_rappers"],
    "Canadian female": ["https://en.wikipedia.org/wiki/Category:Canadian_female_rappers"],
    "German female": ["https://en.wikipedia.org/wiki/Category:German_female_rappers"],
    "South Korean female": ["https://en.wikipedia.org/wiki/Category:South_Korean_female_rappers"],
    "Australian male": ["https://en.wikipedia.org/wiki/Category:Australian_male_rappers"],
    "English male": ["https://en.wikipedia.org/wiki/Category:English_male_rappers"],
    "Canadian male": ["https://en.wikipedia.org/wiki/Category:Canadian_male_rappers"],
    "Mexican male": ["https://en.wikipedia.org/wiki/Category:Mexican_male_rappers"],
    "Nigerian male": ["https://en.wikipedia.org/wiki/Category:Nigerian_male_rappers"],
    "South Korean male": ["https://en.wikipedia.org/wiki/Category:South_Korean_male_rappers"],
    "Spanish male": ["https://en.wikipedia.org/wiki/Category:Spanish_male_rappers"],
    "French unknown": ["https://en.wikipedia.org/wiki/Category:French_rappers"],
    "South African unknown": ["https://en.wikipedia.org/wiki/Category:South_African_rappers"],
    }

def get_wiki_category_names(link_list):
    artist_list = []
    for link in link_list:
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
                artist_list.append(artist_name)
            else:
                artist_list.append(artist.text)
    return artist_list

def create_artist_gender_ethnicity_dict():
    artist_gender_ethnicity_dict = {}
    for key, val in WIKI_CATEGORIES.items():
        artist_gender_ethnicity_dict[key] = get_wiki_category_names(val)
    return artist_gender_ethnicity_dict


def get_gender_and_ethnicity():
    songs = pd.read_json('gender_ethnicity_test_file.json', orient='table')
    artists = list(songs["Artist"])
    genders = list(songs["Gender"])
    ethnicities = list(songs["Ethnicity"])
    names = list(songs["Song"])
    album_dates = {}
    check_song_later = {}
    check_album_later = {}


if __name__ == "__main__":
    print(create_artist_gender_ethnicity_dict())
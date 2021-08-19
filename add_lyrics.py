# FILE: add_lyrics.py.py
# WRITER:lee matan,leem72,207378803
# EXERCISE:intro2cse final_project_rap 2020
# DESCRIPTION:
# NOTES:
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

SIGNS = ['.', ',', ':', ';', '!', '?', '*', '#', '@', '&', '-', '(', ')',
         '[', ']', '{', '}']
COLUMNS = ["Song", "Artist", "Gender", "Album", "Date", "URL", "Profanities"]


def get_one_song_lyrics(song_url):
    """

    :param song_url: A url for one song's web page
    :return: The song's lyrics - ......
    """
    html = requests.get(song_url).text
    soup = BeautifulSoup(html, 'html.parser')
    # first we scrape the full details for the song
    # Some songs have the text and some other stuff
    try:
        details = soup.find('pre').text.split('\n')
    # While some have only text
    except AttributeError:
        details = soup.text.split('\n')
    if details[0] == "":
        details = details[1:]
    # then we separate the song's lyrics into a variable
    song_lyrics = details[5:]
    print(song_lyrics[0:3])
    return song_lyrics


def process_lyrics(one_lyrics):
    """

    :param one_lyrics: A list of strings, each representing one line of the song.
    :return: A list of strings, each representing one word of the song. Without
     song parts indicators (Chorus, verse)
    """
    song_words_list = []
    pattern = "\b[a-zA-Z0-9_]+('||)\b"
    for line in one_lyrics:
        if line == "":
            continue
        elif line[0] == "[" and line[-1] == "]":
            continue
        words = line.split(" ")
        clean_words = []
        for word in words:
            if "[" in word and "]" in word:
                continue
            print(word)
            if word and word[0] in SIGNS:
                word = word[1:]
            if word and word[-1] in SIGNS:
                word = word[:-1]
            clean_words.append(word)
        song_words_list.extend(clean_words)
    return song_words_list


def add_songs_lyrics_to_data(json_file):
    songs_data = pd.read_json(json_file, orient='table')
    all_lyrics = []
    all_url = songs_data['URL']
    for url in all_url:
        lyrics = get_one_song_lyrics(url)
        lyrics_words = process_lyrics(lyrics)
        all_lyrics.append(lyrics_words)
    songs_data['Lyrics'] = all_lyrics
    songs_data.to_json('songs_dt_1808_new.json', orient='table', indent=4)
    print("done")


if __name__ == '__main__':
    add_songs_lyrics_to_data("songs_dt_1808.json")
    ex_ly = ["I bought a big brown teddy bear", "[verse X2]", "Hello world", "[Chorus]"]
    print(process_lyrics(ex_ly))

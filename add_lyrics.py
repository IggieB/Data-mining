# FILE: add_lyrics.py.py
# WRITER:lee matan,leem72,207378803
# EXERCISE:intro2cse final_project_rap 2020
# DESCRIPTION:
# NOTES:
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import sys

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
            clean_word = re.search(r"[\w]+\W{0,1}[\w]+", word)
            if clean_word:
                clean_words.append(clean_word[0])
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
    songs_data.to_json(json_file, orient='table', indent=4)
    print("done")


def divide_json_files(file):
    name_idx = 69
    full_file = pd.read_json(file, orient='table')
    print(full_file)
    df_1 = full_file.iloc[:1112:]
    df_2 = full_file.iloc[1112:2224]
    df_3 = full_file.iloc[2224:3336:]
    df_4 = full_file.iloc[3336::]
    df_list = [df_1, df_2, df_3, df_4]
    for single_df in df_list:
        single_df.reset_index(drop=True, inplace=True)
        single_df.to_json('songs_dt_part_' + str(name_idx) + ".json",
                         orient='table', indent=4)
        name_idx += 1

if __name__ == '__main__':
    for i in range(37, 45):
        print(add_songs_lyrics_to_data('songs_dt_part_' +  str(i) + '.json'))

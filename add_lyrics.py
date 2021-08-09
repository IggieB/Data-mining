# FILE: add_lyrics.py.py
# WRITER:lee matan,leem72,207378803
# EXERCISE:intro2cse final_project_rap 2020
# DESCRIPTION:
# NOTES:
from bs4 import BeautifulSoup
import requests
import pandas as pd

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
    return song_lyrics


def add_songs_lyrics_to_data(json_file):
    songs_data = pd.read_json(json_file, orient='table', indent=4)
    all_lyrics = []
    all_url = songs_data['URL']
    for url in all_url:
        lyrics = get_one_song_lyrics(url)
        all_lyrics.append(lyrics)
    songs_data['Lyrics'] = all_lyrics
    songs_data.to_json('songs_dt5_wLyrics.json', orient='table', indent=4)


if __name__ == '__main__':
    add_songs_lyrics_to_data("songs_dt4.json")

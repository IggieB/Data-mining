from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_dates(url):
    songs = pd.read_json('songs_dt.json', orient='table')
    dates = []
    album_dates = {}
    albums = songs["Album"]
    artists = songs["Artist"]
    rap_albums = []
    for index in range(1, 35):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        rap_albums = rap_albums + soup.find_all('div', class_="itemview")[:499]
        url = "https://www.rapmusicguide.com/browse/p/6/sb/ar|ASC|500|" + \
              str(index)
    for index in range(len(albums)):
        if albums[index].upper() not in album_dates:
            for rap_album in rap_albums:
                album_dates[albums[index].upper()] = None
                if albums[index].split('(')[0].upper() in \
                        rap_album.find_all('a')[1].text.upper() and artists[
                        index] in rap_album.find_all('a')[0].text.upper():
                    album_site = rap_album.find_all('a')[1].get('href')
                    html = requests.get(album_site).text
                    soup = BeautifulSoup(html, 'html.parser')
                    try:
                        year = int(soup.find('p').text.split('Year: ')[1][:4])
                    except IndexError:
                        year = None
                    album_dates[albums[index].upper()] = year
                    rap_albums.remove(rap_album)
                    break
        dates.append(album_dates[albums[index].upper()])
    songs = songs.assign(Date=dates)
    songs.to_json('songs_dt2.json', orient='table', indent=4)


get_dates('https://www.rapmusicguide.com/browse/sb/ar%7CASC%7C500%7C0')
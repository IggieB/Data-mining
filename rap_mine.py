from bs4 import BeautifulSoup
import requests
import pandas as pd

SIGNS = ['.', ',', ':', ';', '!', '?', '*', '#', '@', '&', '-', '(', ')',
         '[', ']', '{', '}']
COLUMNS = ["Song", "Artist", "Gender", "Album", "Date", "URL",
           "Profanities"]
OHHLA_SITE = ' http://ohhla.com/'


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


def get_links_from_ugly(url, soup, lst):
    """
    Read links from relatively 'naked' menu pages, for albums and the songs
    in the albums
    :param lst:
    :param url: The address of the menu page
    :param soup: The content of that menu page
    :return: A list of links to the texts of the songs
    """
    text_links = []
    links = soup.find_all('tr')[3:-1]
    for link in links:
        new_link = url + link.find('a').get('href')
        if new_link[-4:] != '.txt':
            html = requests.get(new_link).text
            soup = BeautifulSoup(html, 'html.parser')
            text_links += get_links_from_ugly(new_link, soup, lst)
        else:
            if new_link not in lst:
                text_links.append(new_link)
    return text_links


def find_all_songs(url):
    """
    Gets the links to the songs of all the artists with a page on the site
    :param url: The address of the list of artists
    :return: A list of all the links to all the songs
    """
    used_menus = [url]
    artists = []
    lyric_links = []
    while True:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find('pre').find_all('a')[1:]
        for link in links:
            # in case the line is empty
            if link.get('href') is None:
                continue
            artists.append(OHHLA_SITE + str(link.get('href')))
        # The next lines are for moving between the pages to get all the
        # artists
        # menus = soup.find('h3').find_all('a')
        # for menu in menus:
        #    link = menu.get('href')
        #    if '#' in link or (OHHLA_SITE + link) in used_menus:
        #        continue
        #    else:
        #        url = OHHLA_SITE + link
        #        used_menus.append(url)
        #        break
        break
    for artist in artists:
        html = requests.get(artist).text
        soup = BeautifulSoup(html, 'html.parser')
        # Ugly menu pages do not have the item 'br' in them. I am using that
        # fact to find those ugly menu pages
        if soup.find('br') is None:
            lyric_links += get_links_from_ugly(artist, soup, lyric_links)
        # 'Prettier' pages have tables for the artist's albums, with links to
        # the songs in those tables
        else:
            try:
                albums = soup.find('table').find_all('table')[1:]
            except AttributeError:
                # Usually a bad link can come from not having an .html at the
                # end
                try:
                    artist = soup.find('meta').get('content').split('URL=')[1]
                    html = requests.get(artist).text
                    soup = BeautifulSoup(html, 'html.parser')
                    albums = soup.find('table').find_all('table')[1:]
                # Otherwise, there are some broken links, and they cannot be
                # helped
                except IndexError:
                    continue
            for album in albums:
                songs = album.find_all('tr')[2:]
                for song in songs:
                    try:
                        if OHHLA_SITE + song.find('a').get('href') not in \
                                lyric_links:
                            lyric_links.append(OHHLA_SITE + song.find(
                                'a').get('href'))
                    except AttributeError:
                        continue
    return lyric_links


def find_profanities(lyrics, profanities):
    """
    Finds Profanities within a song
    :param lyrics: The song's text
    :param profanities: A list of profane words
    :return: A dictionary of profanities and the No. of times they were shown
    """
    words = []
    used_swears = {}
    # Taking the song's text and putting it in a list
    for line in lyrics:
        line = line.split(' ')
        words += line
    for word in words:
        for sign in SIGNS:
            if sign in word:
                word.replace(sign, '')
        if word in profanities:
            if word not in used_swears:
                used_swears[word] = 1
            else:
                used_swears[word] += 1
    return used_swears


def data_profanities(url):
    songs_dt = pd.DataFrame(columns=COLUMNS)
    songs = find_all_songs(url)
    all_profanities = read_wordlist_file('bad-words.txt')
    artist_genders = {}
    for song in songs:
        html = requests.get(song).text
        soup = BeautifulSoup(html, 'html.parser')
        # Some songs have the text and some other stuff
        try:
            details = soup.find('pre').text.split('\n')
        # While some have only text
        except AttributeError:
            details = soup.text.split('\n')
        if details[0] == "":
            details = details[1:]
        artist = \
            details[0].replace('Artist: ', '').split(' f/ ')[0].split(' x ')[
                0].split(' + ')[0].upper()
        # If the song is empty, the loop will continue
        try:
            album = details[1].replace('Album:  ', '')
        except IndexError:
            continue
        if artist not in artist_genders:
            artist_page = 'https://en.wikipedia.org/wiki/' + \
                          artist.replace(' ', '_')
            html = requests.get(artist_page).text
            soup = BeautifulSoup(html, 'html.parser')
            tags = str(soup.find('script')).split(',')
            artist_genders[artist] = 'M?'
            for tag in tags:
                if 'female' in tag or 'Female' in tag or 'Women' in tag or \
                        'women' in tag or 'Woman' in tag or 'woman' in tag:
                    artist_genders[artist] = 'F'
                    break
                elif 'male' in tag or 'Male' in tag or 'Man' in tag or 'man' \
                        in tag or 'Men' in tag or 'men' in tag:
                    artist_genders[artist] = 'M'
                    break
        song_name = details[2].replace('Song:   ', '')
        song_lyrics = details[5:]
        profanities = find_profanities(song_lyrics, all_profanities)
        gender = artist_genders[artist]
        ethnicity = "Unknown"
        date = None
        song_details = [song_name, artist, gender, ethnicity ,album, date,
                        song, profanities]
        songs_dt = songs_dt.append(pd.DataFrame(columns=COLUMNS,
                                                data=[song_details]))
    songs_dt.reset_index(drop=True, inplace=True)
    songs_dt.to_json('songs_dt5.json', orient='table', indent=4)


if __name__ == "__main__":
    data_profanities('http://ohhla.com/all_five.html')

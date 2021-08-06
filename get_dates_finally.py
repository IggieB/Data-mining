from selenium.common.exceptions import ElementClickInterceptedException, \
    NoSuchElementException, WebDriverException
from selenium import webdriver as wb
import pandas as pd
NIKUDS = ['.', ',', ':', ';', '!', '?', ' &']


webD = wb.Chrome('chromedriver.exe')


def get_album_lst():
    songs = pd.read_json('songs_dt5.json', orient='table')
    dates = list(songs['Date'])
    albums = list(songs["Album"])
    artists = list(songs["Artist"])
    names = list(songs["Song"])
    album_dates = {}
    check_song_later = {}
    check_album_later = {}
    try:
        for index in range(len(songs)):
            print(dates[index])
            org_alb = albums[index].lower().split(' (')[0]
            album = org_alb
            if albums[index] in album_dates:
                dates[index] = album_dates[albums[index]]
                continue
            elif albums[index] in check_album_later:
                dates[index] = check_album_later[albums[index]]
                continue
            for nikud in NIKUDS:
                album = album.replace(nikud, '')
            for letter in album:
                if 97 > ord(letter) or 122 < ord(letter):
                    if 48 > ord(letter) or 57 < ord(letter):
                        album = album.replace(letter, '-')
            album = album.replace('--', '')
            rtists = artists[index].lower().split(' feat')[0]\
                .replace(' x ', ' & ').split(
                ' &')
            for ind in range(len(rtists)):
                rtists[ind] = rtists[ind].split(' (')[0]
            art = ''
            for artist in rtists:
                for nikud in NIKUDS:
                    artist = artist.replace(nikud, '')
                arts = artist.split(' ')
                for ar in arts:
                    art = art + ar + '-'
                art = art + 'and'
            art = art[:-4]
            songname = names[index].lower().split(' (')[0]
            for nikud in NIKUDS:
                songname = songname.replace(nikud, '')
            for letter in songname:
                if 97 > ord(letter) or 122 < ord(letter):
                    if 48 > ord(letter) or 57 < ord(letter):
                        songname = songname.replace(letter, '-')
            url = 'https://genius.com/artists/' + art
            webD.get(url)
            webD.find_element_by_xpath(
                '/html/body/routable-page/ng-outlet/routable-profile-page/ng'
                '-outlet/routed-page/profile-page/div[3]/div['
                '2]/artist-songs-and-albums/album-grid/div[2]').click()
            albs = webD.find_elements_by_class_name(
                'mini_card-title_and_subtitle')
            for alb in albs:
                alb_name = alb.find_element_by_class_name(
                    'mini_card-title').text.lower()
                alb_date = alb.find_element_by_class_name(
                    'mini_card-subtitle').text
                album_dates[alb_name] = alb_date
                cont = 0
                for key in album_dates.keys():
                    if org_alb in key or key in org_alb:
                        dates = album_dates[key]
                        cont = 1
                        break
                if cont == 1:
                    continue
                else:
                    url = 'https://genius.com/' + art
    except IndexError:
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt5.json', orient='table', indent=4)
    songs = songs.assign(Date=dates)
    songs.to_json('songs_dt5.json', orient='table', indent=4)


if __name__ == "__main__":
    get_album_lst()
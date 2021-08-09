from selenium.common.exceptions import ElementClickInterceptedException, \
    NoSuchElementException
from selenium import webdriver as wb
import pandas as pd

webD = wb.Chrome('chromedriver.exe')


def get_dates():
    songs = pd.read_json('songs_dt.json', orient='table')
    dates = []
    album_dates = {}
    albums = songs["Album"]
    artists = songs["Artist"]
    start = 0
    for index in range(len(albums)):
        if albums[index] not in album_dates:
            webD.get(
                'https://www.discogs.com/search/?q=' + albums[
                    index].split('(')[0].replace(
                    ' ', '+') + '+' + artists[index].replace(' ', '+') +
                '&type=release')
            if start == 0:
                webD.find_element_by_xpath('/html/body/div[6]/div[3]/div/div['
                                           '1]/div/div[2]/div/button[2]'
                                           '').click()
                webD.find_element_by_xpath(
                    '/html/body/div[6]/div[2]/div[3]/div[1]/button').click()
                start = 1
            try:
                webD.find_element_by_xpath('/html/body/div[1]/div[4]/div['
                                           '3]/div[3]/div[2]/div[1]/h4/'
                                           'a').click()
                year = int(webD.find_element_by_xpath('/html/body/div['
                                                      '1]/div/div['
                                                      '3]/div[1]/div['
                                                      '14]/div/div[2]/ '
                                                      'div[4]/div[2]/a/'
                                                      'time').text[
                           -4:])
                if year < 1990:
                    year = None
            except ElementClickInterceptedException:
                year = None
            except NoSuchElementException:
                year = None
            dates.append(year)
            album_dates[albums[index]] = year
        else:
            dates.append(album_dates[albums[index]])
    songs = songs.assign(Date=dates)
    songs.to_json('songs_dt2.json', orient='table', indent=4)


get_dates()

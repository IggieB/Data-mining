from selenium.common.exceptions import ElementClickInterceptedException, \
    NoSuchElementException, WebDriverException
from selenium import webdriver as wb
import pandas as pd


webD = wb.Chrome('chromedriver.exe')


def get_dates():
    songs = pd.read_json('songs_dt.json', orient='table')
    dates = list(songs['Date'])
    albums = songs["Album"]
    artists = songs["Artist"]
    found_albums = {}
    start = 0
    try:
        for index in range(len(albums)):
            if type(dates[index]) is not int and type(dates[index]) is not \
                    float:
                continue
            elif albums[index].upper() not in found_albums:
                webD.get('https://www.discogs.com/search/?q=' + albums[index].split(
                    '(')[0].replace(' ', '+') + '+' + artists[index].replace(
                    ' ', '+') + '&type=release&layout=sm')
                if start == 0:
                    webD.find_element_by_xpath('/html/body/div[6]/div[3]/div/div['
                                               '1]/div/div[2]/div/button[2]').click()
                    webD.find_element_by_xpath(
                        '/html/body/div[6]/div[2]/div[3]/div[1]/button').click()
                    start = 1
                try:
                    year = int(webD.find_element_by_class_name('card_release_year').text[-4:])
                    if year < 1980:
                        year = None
                except ElementClickInterceptedException:
                    year = None
                except NoSuchElementException:
                    year = None
                found_albums[albums[index].upper()] = year
                dates[index] = year
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt2.json', orient='table', indent=4)
    except WebDriverException:
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt2.json', orient='table', indent=4)


if __name__ == "__main__":
    get_dates()

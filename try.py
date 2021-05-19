from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from selenium import webdriver as wb
import pandas as pd

decades = ['1980', '1990', '2000', '2010', '2020']

webD = wb.Chrome('chromedriver.exe')


def get_dates():
    songs = pd.read_json('songs_dt.json', orient='table')
    dates = list(songs["Date"])
    albums = songs["Album"]
    start = 0
    try:
        for decade in decades:
            for num in range(0, 10):
                album_names = []
                year = decade[:3]+str(num)
                print(year)
                if year == '2022':
                    break
                url = 'https://www.discogs.com/search/?limit=250&genre_exact' \
                      '=Hip+Hop&decade=' + decade + '&year=' + year + \
                      '&layout=sm&type=release'
                while True:
                    webD.get(url)
                    if start == 0:
                        webD.find_element_by_xpath(
                            '/html/body/div[6]/div[3]/div/div['
                            '1]/div/div[2]/div/button[2]').click()
                        webD.find_element_by_xpath(
                            '/html/body/div[6]/div[2]/div[3]/div[1]/button').click()
                        start = 1
                    for name in webD.find_elements_by_class_name(
                            'search_result_title'):
                        album_names.append(name.text.split(' (')[0].upper())
                    try:
                        url = webD.find_element_by_class_name(
                            'pagination_next').get_attribute('href')
                    except NoSuchElementException:
                        break
                for index in range(len(albums)):
                    if albums[index].split(' (')[0].upper() in album_names:
                        if type(dates[index]) is not float and type(dates[index]) is not float:
                            dates[index] = int(year)
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt2.json', orient='table', indent=4)
    except WebDriverException:
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt2.json', orient='table', indent=4)



get_dates()

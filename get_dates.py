from selenium.common.exceptions import ElementClickInterceptedException, \
    NoSuchElementException, WebDriverException
from selenium import webdriver as wb
import pandas as pd
import time


webD = wb.Chrome('chromedriver.exe')


def get_dates():
    try:
        #TODO: we changed the file to part 1 just to delete old files!
        songs = pd.read_json('songs_dt_part_1.json', orient='table')
    except AssertionError as err:
        raise err
    dates = list(songs['Date'])
    albums = songs["Album"]
    artists = songs["Artist"]
    found_albums = {}
    start = 0
    try:
        for index in range(len(albums)):
            if 48 <= ord(str(dates[index])[0]) <= 57:
                continue
            if str(albums[index]).lower() not in found_albums:
                webD.get(
                    'https://www.discogs.com/search/?q=' + str(albums[
                        index]).split('(')[0].replace(' ', '+') + '+' + str(
                        artists[index]).replace(' ', '+') +
                    '&type=release&layout=sm')
                if start == 0:
                    time.sleep(2)
                    webD.find_element_by_xpath(
                        '/html/body/div[5]/div[2]/div/div[1]/div/div[2]/div/button[2]').click()
                    time.sleep(2)
                    webD.find_element_by_xpath(
                        '/html/body/div[5]/div[3]/div[3]/div[1]/button').click()
                    start = 1
                try:
                    card = webD.find_element_by_class_name('card_body')
                    title = card.find_element_by_tag_name('h4').text.lower()
                    if str(albums[index]).lower().split(' (')[0] not in title:
                        if str(artists[index]).lower().split(' (')[0] not in \
                                title:
                            continue
                    year = card.find_element_by_class_name(
                        'card_release_year').text[-4:]
                    if int(year) < 1980:
                        year = None
                except ElementClickInterceptedException:
                    year = None
                except NoSuchElementException:
                    year = None
                found_albums[str(albums[index]).lower()] = year
            dates[index] = found_albums[str(albums[index]).lower()]
            print(str(dates[index])[0])
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt_part_1.json', orient='table', indent=4)
    except WebDriverException:
        songs = songs.assign(Date=dates)
        songs.to_json('songs_dt_part_1.json', orient='table', indent=4)


if __name__ == "__main__":
    get_dates()
from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_genders(female_rappers_nations, male_rappers_nations, file_name):
    songs = pd.read_json(file_name, orient='table')
    artists = list(songs['Artist'])
    genders = list(songs['Gender'])
    female_rappers = []
    html = requests.get(female_rappers_nations).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', class_='mw-content-ltr')[-1].find_all('a')
    for page in pages:
        female_rappers_lst = page.get('href')
        html = requests.get('https://en.wikipedia.org'
                            + female_rappers_lst).text
        soup = BeautifulSoup(html, 'html.parser')
        females = soup.find_all('div', class_='mw-content-ltr')[-1].find_all('a')
        for female in females:
            female_rappers.append(female.text.split(' (')[0].upper())
        maybe_next = soup.find('div', id='mw-pages').find_all('a')[-1]
        while maybe_next.text == 'next page':
            maybe_next = maybe_next.get('href')
            html = requests.get('https://en.wikipedia.org' + maybe_next).text
            soup = BeautifulSoup(html, 'html.parser')
            females = soup.find_all('div', class_='mw-content-ltr')[-1].find_all(
                'a')
            for female in females:
                female_rappers.append(female.text.split(' (')[0].upper())
            maybe_next = soup.find('div', id='mw-pages').find_all('a')[-1]
    for index in range(len(artists)):
        if artists[index] in female_rappers:
            genders[index] = 'F'
        else:
            genders[index] = '?M'
    male_rappers = []
    html = requests.get(male_rappers_nations).text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', class_='mw-content-ltr')[-1].find_all('a')
    for page in pages:
        female_rappers_lst = page.get('href')
        html = requests.get('https://en.wikipedia.org'
                            + female_rappers_lst).text
        soup = BeautifulSoup(html, 'html.parser')
        males = soup.find_all('div', class_='mw-content-ltr')[-1].find_all('a')
        for male in males:
            male_rappers.append(male.text.split(' (')[0].upper())
        maybe_next = soup.find('div', id='mw-pages').find_all('a')[-1]
        while maybe_next.text == 'next page':
            maybe_next = maybe_next.get('href')
            html = requests.get('https://en.wikipedia.org' + maybe_next).text
            soup = BeautifulSoup(html, 'html.parser')
            males = soup.find_all('div', class_='mw-content-ltr')[-1].find_all(
                'a')
            for male in males:
                male_rappers.append(male.text.split(' (')[0].upper())
            maybe_next = soup.find('div', id='mw-pages').find_all('a')[-1]
    for index in range(len(artists)):
        if artists[index] in male_rappers:
            genders[index] = 'M'
    songs = songs.assign(Gender=genders)
    songs.to_json(file_name, orient='table', indent=4)


get_genders('https://en.wikipedia.org/wiki/Category:Female_rappers_by_nationality', 'https://en.wikipedia.org/wiki/Category:Male_rappers_by_nationality', 'songs_dt.json')
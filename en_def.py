import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_en_def(char):
    url = f'https://koreanhanja.app/{urllib.parse.quote(char)}'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve English definitions
    page = urlopen(f'https://koreanhanja.app/{urllib.parse.quote(char)}')
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    try:
        td = soup.find_all('td', class_=None)[0].get_text()
        meaning_e = ' '.join(re.findall(r'([a-z]+.?\s?)', td))
    except IndexError:
        meaning_e = 'English definition unavailable.'
        print('Encountered error when retrieving English definition.')

    return meaning_e


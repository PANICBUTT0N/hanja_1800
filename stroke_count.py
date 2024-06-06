import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_stroke_count(char):
    page = urlopen(f'https://www.strokeorder.com/chinese/{urllib.parse.quote(char)}')
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    try:
        strokes = soup.find_all('div', class_='stroke-hanzi-info-right')[1].get_text()
        strokes = strokes.replace('strokes', '').strip()
        return strokes
    except IndexError:
        try:
            page = urlopen(f'http://hanzidb.org/character/{urllib.parse.quote(char)}')
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all('p')

            match = re.findall(r'\d+', tags[2].get_text())
            return match[0]
        except:
            print('Encountered error when retrieving stroke count.')
            return 'Could not retrieve stroke count.'


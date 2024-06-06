from bs4 import BeautifulSoup
import urllib.parse
from urllib.request import urlopen


def get_radicals(char):
    url = f'https://koreanhanja.app/{urllib.parse.quote(char)}'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Retrieving the radicals
    div = soup.find("div", class_='radicals')
    anchors = [anchor.get_text() for anchor in div.find_all('a')]
    radicals = ', '.join(anchors)

    return radicals

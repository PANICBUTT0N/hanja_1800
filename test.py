from bs4 import BeautifulSoup
import urllib.parse
from urllib.request import urlopen

import re

page = urlopen(f'http://hanzidb.org/character/{urllib.parse.quote('于')}')
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

tags = soup.find_all('p')

match = re.findall(r'\d+', tags[2].get_text())

print(match[0])
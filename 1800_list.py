# Scrapes the list of 1800 Hanja and creates list of 
from bs4 import BeautifulSoup
import csv
from openpyxl import Workbook
import re
import urllib.parse
from urllib.request import Request, urlopen
from wordfreq import zipf_frequency
from level_getter import *
import time
alternates = {1: '"차 차"로도 읽는다.',
              2: '"거북 귀", "터질 균"으로도 읽는다.',
              3: '"성 김"으로도 읽는다.',
              4: '"헤아릴 탁"으로도 읽는다.',
              5: '"노래 악", "좋아할 요"로도 읽는다.',
              6: '"거느릴 솔"로도 읽는다.',
              7: '"다시 부"로도 읽는다.',
              8: '"푼 푼"으로도 읽는다.',
              9: '"아닐 부"로도 읽는다.',
              10: '"덜 생"으로도 읽는다.',
              11: '"미워할 오"로도 읽는다.',
              12: '"쉬울 이"로도 읽는다.',
              13: '"곧 즉"으로도 읽는다.',
              14: '"홉 홉"으로도 읽는다.'
              }

url = (
    'https://ko.wiktionary.org/wiki/%EB%B6%80%EB%A1%9D:%ED%95%9C%EB%AC%B8_%EA%B5%90%EC%9C%A1%EC%9A%A9_%EA%B8%B0%EC%B4'
    '%88_%ED%95%9C%EC%9E%90_1800')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKi'
                         't/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
req = Request(url, headers=headers)
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

tags = soup.find_all('td')  # Finds all the td tags
tags = [tag.get_text().replace('\n', '') for tag in tags]
del tags[:4]  # First 3 are irrelevant
tags = [i for i in tags if i]  # Clears empty entries
tags = [entry for entry in tags if 'ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ' not in entry]  # Gets rid of page navigator.
tags = [entry.split('•')for index, entry in enumerate(tags)]  # Splits up these individual entry chunks from each cell
# into individual entries

# Creates list of each entry, with hanja, definition, and group. Space delimited.
list_1800 = [thing.strip().replace('(', '').replace(')', '') for item in tags for thing in item]
list_1800 = [entry.split() for index, entry in enumerate(list_1800)]  # Makes each entry a nested list

# Merges multiple definitions
for entry in list_1800:
    if len(entry) > 3:
        merged_value = ", ".join(entry[1:-1])
        del entry[1:-1]
        entry.insert(1, merged_value)

for entry in list_1800:
    entry[1], entry[2] = entry[2], entry[1]  # Moves pronunciation to the middle
    # Locates alternate pronunciations and adds them to the fourth cell in the entry
    if '[' in entry[1]:
        brackets = re.findall(r'\[[^\]]*\]', entry[1])[0]
        index = re.findall(r'\[(.*?)]', entry[1])[0]
        entry[1] = entry[1].replace(brackets, '')
        entry.append(alternates[int(index)])
    else:
        entry.append('')

# KHA Requests
for index, entry in enumerate(list_1800[0:3]):
    for char in list_1800[index][0]:
        url = f'https://koreanhanja.app/{urllib.parse.quote(char)}'
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Retrieving the radicals
        div = soup.find("div", class_='radicals')
        anchors = [anchor.get_text() for anchor in div.find_all('a')]
        radicals = ', '.join(anchors)

        # Retrieving the examples
        similar_words = {}
        table = soup.find('table', class_='similar-words')
        for tr in table.find_all('tr'):
            td_tags = [td.get_text().replace('\t', '').replace('\n', '').replace('\xa0', ' ')
                       .replace('(conjugate verb)', '') for td in tr.find_all('td')]
            similar_words.update({td_tags[1]: td_tags[::2]})
        # Chooses the top 6 examples based on word frequency
        for entry_index, word in enumerate(similar_words):
            similar_words[word].append(zipf_frequency(word, 'ko'))
        similar_words = {k: v for k, v in sorted(similar_words.items(), key=lambda item: item[1][2], reverse=True)}
        if len(similar_words) >= 6:
            keys_to_delete = list(similar_words.keys())[6:]
            for key in keys_to_delete:
                del similar_words[key]

        # Add the similar words to list_1800
        example_cell = ''
        for entry_index1, word in enumerate(similar_words):
            examples = []
            [examples.append(part) for part in (similar_words[word][0:2])]
            example_entry = f'{examples[0]} - {word} ({examples[1]})'
            example_cell += example_entry + '\n'

        list_1800[index].append(example_cell)
        list_1800[index].append(radicals)

        # Retrieves 한자 level
        list_1800[index].extend(level for level in get_level(char))
    print(f'Entry {index} processed.')


list_1800.insert(0, ['Hanja', 'Pronunciation', 'Definition', 'Alternate Pronunciation', 'Examples',
                     'Radicals', 'Reading Level', 'Writing Level'])

wb = Workbook()
ws = wb.active

with open('hanja.csv', 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(list_1800)

for row, entry in enumerate(list_1800):
    for column, part in enumerate(entry):
        ws.cell(row + 1, column + 1).value = part
wb.save('Hanja.xlsx')

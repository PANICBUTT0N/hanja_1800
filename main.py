# Scrapes the list of 1800 Hanja and creates list of 
from bs4 import BeautifulSoup
import csv
from openpyxl import Workbook
from urllib.request import Request, urlopen
from levels import *
from radicals import get_radicals
from examples import get_examples
from stroke_count import get_stroke_count
from en_def import get_en_def

alternates = {1: '차',
              2: '거북, 귀',
              3: '성, 김',
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
    'https://ko.wiktionary.org/wiki/%EB%B6%80%EB%A1%9D:%ED%95%9C%EB%AC%B8_%EA%B5%90%EC%9C%A1%EC%9A%A9_%EA%B8%B0%EC%B4%8'
    '8_%ED%95%9C%EC%9E%90_1800')
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
tags = [entry.split('•')for entry in tags]  # Splits up these individual entry chunks from each cell
# into individual entries

# Creates list of each entry, with hanja, definition, and group. Space delimited.
list_1800 = [thing.strip().replace('(', '').replace(')', '') for item in tags for thing in item]
list_1800 = [entry.split() for entry in list_1800]  # Makes each entry a nested list

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

# Additional data requests. See modules for details.
for index, entry in enumerate(list_1800[0:2]):
    for char in entry[0]:
        list_1800[index].append(get_examples(char))
        list_1800[index].append(get_radicals(char))
        list_1800[index].extend(level for level in get_level(char))
        list_1800[index].append(get_stroke_count(char))
        list_1800[index].append(get_en_def(char))

    print(f'Entry {index + 1} processed.')

list_1800.insert(0, ['Hanja', 'Pronunciation', 'Meaning_K', 'Alternate Pronunciation', 'Examples',
                     'Radicals', 'Reading Level', 'Writing Level', 'Strokes', 'Meaning_E'])

wb = Workbook()
ws = wb.active

with open('hanja1.csv', 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(list_1800)

for row, entry in enumerate(list_1800):
    for column, part in enumerate(entry):
        ws.cell(row + 1, column + 1).value = part
wb.save('Hanja1.xlsx')

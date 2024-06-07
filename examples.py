from bs4 import BeautifulSoup
import urllib.parse
from urllib.request import urlopen
from wordfreq import zipf_frequency


def get_examples(char):
    page = urlopen(f'https://koreanhanja.app/{urllib.parse.quote(char)}')
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
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

    # Retrieve  similar words
    example_cell = ''
    for entry_index1, word in enumerate(similar_words):
        examples = []
        [examples.append(part) for part in (similar_words[word][0:2])]
        example_entry = f'{examples[0]} - {word} ({examples[1]})'
        example_cell += example_entry + '\n'

    return example_cell

print(get_examples('人'))

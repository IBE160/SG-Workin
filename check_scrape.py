import requests
from bs4 import BeautifulSoup

url = 'https://www.himolde.no/studier/programmer/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

program_cards = soup.find_all('div', class_='vrtx-card-body')

if not program_cards:
    print('No program cards found. Content might be loaded via JavaScript.')
else:
    print('Found program cards. Extracting titles:')
    for card in program_cards:
        title = card.find('h3')
        if title:
            print(title.get_text().strip())
        else:
            print('  - H3 title not found in card.')

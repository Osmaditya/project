import requests
from bs4 import BeautifulSoup

def query():
    user_query = input('Enter your query: ')
    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        result = soup.find('div', class_='BNeawe').get_text()
        print(result)
    except AttributeError:
        print('Sorry, no result found, please be clear.')

while True:
    query()
    user_input = input('To continue press y: ')
    if user_input.lower() != 'y':
        break

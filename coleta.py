import time
import random
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Configurações do Firefox driver
driver = webdriver.Firefox()
options = webdriver.FirefoxOptions()
options.add_argument('start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')

# Acessa a página de resultados da busca
url = 'https://www.tripadvisor.com.br/Search?geo=303441&q=restaurante&queryParsed=true&searchSessionId=0011633f21f0c492.ssid&searchNearby=false&sid=28B8593E5467463C9F037D6A034A5E081680103846830&blockRedirect=true&rf=4&ssrc=m&o=30'
driver.get(url)

# Espera até que a página carregue completamente
time.sleep(random.randint(5, 15))

# Coleta os links para as cinco primeiras páginas de restaurante na página de resultados da busca
local_links = []
soup = BeautifulSoup(driver.page_source, 'html.parser')
for link in soup.find_all('a', {'class': 'review_count'}):
    local_links.append(link['href'])

# Coleta as informações dos locais em cada página de local
locais = []
for link in local_links:
    driver.get('https://www.tripadvisor.com.br' + link)

    # Espera até que a página carregue completamente
    time.sleep(random.randint(10, 25))

    # Coleta as informações do local
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    try:
        name = soup.find('h1', {'class': 'HjBfq'}).text
    except AttributeError:
        name = None

    try:
        phone = soup.find('a', {'class': 'yEWoV'}).text
    except AttributeError:
        phone = None

    try:
        address = soup.find('span', {'class': 'yEWoV'}).text
    except AttributeError:
        address = None

    try:
        cuisine_div = soup.find('div', {'class': 'UrHfr'}).find('div', text='COZINHAS')
        cuisine = cuisine_div.find_next_sibling('div').text
    except AttributeError:
        cuisine = None

    try:
        price_div = soup.find('div', {'class': 'UrHfr'}).find('div', text='FAIXA DE PREÇO')
        price = price_div.find_next_sibling('div').text
    except AttributeError:
        cuisine = None

    try:
        total_reviews = soup.find('span', {'class': 'AfQtZ'}).text.split()[0].replace('.', '')
    except AttributeError:
        total_reviews = None

    try:
        average_rating = soup.find('span', {'class': 'ZDEqb'}).text
    except AttributeError:
        average_rating = None

    # Coleta as avaliações de usuários na página do local
    reviews = []
    review_count = 0
    for review in soup.find_all('div', {'class': 'review-container'}):
        rating = review.find('span', {'class': 'ui_bubble_rating'})[
            'class'][1].split('_')[-1]
        title = review.find('span', {'class': 'noQuotes'}).text
        content = review.find('p', {'class': 'partial_entry'}).text
        date = review.find('span', {'class': 'ratingDate'})['title']
        reviews.append({'rating': rating, 'title': title,
                       'content': content, 'date': date})
    review_count += 1
    if review_count >= 3:
        break

    # Adiciona as informações do local à lista de locais
    local = {
        'name': name,
        'address': address,
        'phone': phone,
        'cuisine': cuisine,
        'price': price,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'reviews': reviews
    }
    locais.append(local)


# Salva as avaliações coletadas em um arquivo JSON externo
with open('locais.json', 'w', encoding='utf-8') as f:
    json.dump(locais, f, ensure_ascii=False)

driver.close()
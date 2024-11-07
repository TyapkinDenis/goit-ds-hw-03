import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Підключення до MongoDB
client = MongoClient(
    "mongodb+srv://denis23:2323@test23.4vwna.mongodb.net/?retryWrites=true&w=majority&appName=Test23",
    server_api=ServerApi('1')
)

# Вибір бази даних
db = client.authors_qoutes


quotes_data = []
authors_data = {}

# Функція для збору цитат і авторів
def scrape_page(page_num):
    url = f'http://quotes.toscrape.com/page/{page_num}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Збираємо всі цитати на сторінці
    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author_name = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]

        # Додаємо цитату до списку
        quotes_data.append({
            "tags": tags,
            "author": author_name,
            "quote": text
        })

        # Збираємо інформацію про авторів, якщо ще не було зібрано
        if author_name not in authors_data:
            author_url = quote.find('a')['href']
            author_details = scrape_author_details('http://quotes.toscrape.com' + author_url)
            authors_data[author_name] = author_details

# Функція для збору інформації про авторів
def scrape_author_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

# Збираємо дані з 10 сторінок 
for page_num in range(1, 11):  
    scrape_page(page_num)

# Вставка авторів в колекцію authors
db.authors.insert_many(list(authors_data.values()))

# Вставка цитат в колекцію quotes
db.quotes.insert_many(quotes_data)

print("Дані успішно зібрано та завантажено.")

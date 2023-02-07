import json
import requests
from bs4 import BeautifulSoup


def extract_data():
    URL = "https://quotes.toscrape.com"
    authors = {}
    quotes = []

    while URL:
        res = requests.get(URL)
        soup = BeautifulSoup(res.text, 'html.parser')

        for quote in soup.find_all('div', class_='quote'):
            quote_text = quote.find('span', class_='text').text.strip()
            author = quote.find('span', class_='author')
            if author:
                author_name = author.text.strip()
            else:
                author_name = None
            tags = [tag.text.strip() for tag in quote.find_all('a', class_='tag')]
            quotes.append({'quote': quote_text, 'author': author_name, 'tags': tags})

            author_url = quote.find('span', class_='author')
            author_url = author_url.find('a')['href'] if author_url else None
            if author_url and author_name not in authors:
                author_res = requests.get(f'https://quotes.toscrape.com{author_url}')
                author_soup = BeautifulSoup(author_res.text, 'html.parser')
                author_birthday = author_soup.find('span', class_='author-born-date')
                author_birthday = author_birthday.text.strip() if author_birthday else None
                author_location = author_soup.find('span', class_='author-born-location')
                author_location = author_location.text.strip() if author_location else None
                author_description = author_soup.find('div', class_='author-description')
                author_description = author_description.text.strip() if author_description else None
                authors[author_name] = {
                    'birthday': author_birthday,
                    'location': author_location,
                    'description': author_description,
                }

        URL = soup.find('li', class_='next')
        if URL:
            URL = URL.find('a')['href']
        else:
            URL = None

    with open('quotes.json', 'w') as f:
        json.dump(quotes, f)

    with open('authors.json', 'w') as f:
        json.dump(authors, f)


if __name__ == '__main__':
    extract_data()
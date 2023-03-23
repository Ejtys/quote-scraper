import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import requests
from bs4 import BeautifulSoup

from models.quoteModel import Quote
from models.authorModel import Author

from scrapers.authorScraper import scrap_author_page

"""Scrapes data from one page of quotes on quotes.toscrape.com."""
def scrape_quote_page(url:str):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    quote_list = get_quotes_html(soup)
    for q in quote_list:
        scrape_quote(q)

def get_quotes_html(soup:BeautifulSoup) -> list:
    return soup.select('.quote')

def scrape_quote(quote_html):
    author = get_author(quote_html)
    tags = get_tags(quote_html)
    quote_str = get_quote(quote_html)

    quote = Quote(author, quote_str)

    for tag in tags:
        quote.add_tag(tag)
    
    print()
    print(quote)
    print(quote.tags)
    

def get_author(quote_html) -> Author:
    author_name = quote_html.select('.author')[0].text.strip()
    if not Author.from_name(author_name):
        link = "http://quotes.toscrape.com/" + quote_html.select('a')[0]['href']
        return scrap_author_page(link)
    a =  Author.from_name(author_name)
    return a

def get_tags(quote_html) -> list[str]:
    return [x.text for x in quote_html.select('.tag')]

def get_quote(quote_html) -> str:
    return quote_html.select('.text')[0].text[1:-1]

scrape_quote_page('https://quotes.toscrape.com/page/1/')
for a in Quote.all():
    print(a)
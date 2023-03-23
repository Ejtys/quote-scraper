import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from scrapers.pageScraper import scrape_quote_page

def crawl():
    for x in range(10):
        scrape_quote_page(f'https://quotes.toscrape.com/page/{x + 1}/')
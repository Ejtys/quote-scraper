import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import requests
from bs4 import BeautifulSoup

from models.locationModel import Location
from models.authorModel import Author


def scrap_author_page(url:str):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    location = get_location(soup)
 
    date = get_date_stamp(soup)

    name = get_name(soup)

    Author(name, location, date)


def get_location(soup:BeautifulSoup) -> Location:
    l = soup.select('.author-born-location')[0].string
    l = l.split(", ")
    city = l[0][3:]
    country = l[-1]
    return Location(city, country)

def get_date_stamp(soup) -> int:
    d = soup.select('.author-born-date')[0].string

    return Author.str_to_timestamp(d)

def get_name(soup) -> str:
    #html is a little bit broken on the page so solution is weird as well.
    return soup.select('h3')[0].text.split('\n')[0].strip()


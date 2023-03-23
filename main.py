from scrapers.crawl import crawl
from models.authorModel import Author
from models.quoteModel import Tag

if __name__ == '__main__':
    crawl()

    for x in Author.all():
        print(x)

    for x in Tag('life').quotes:
        print(x)

    
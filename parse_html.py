import codecs
import csv
import re
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup

from BookParser import BookParser
import pandas as pd

links_books = []
links_authors = []
for i in range(1, 41):
    f = codecs.open("sources\{}.html".format(i), 'r', 'utf-8')
    document = BeautifulSoup(f.read(), "html.parser")
    reg = r'a\s+[^>]*?href="([^"]*)"'
    pattern = re.compile(reg, re.UNICODE)
    list_of_links = pattern.findall(str(document))
    [links_books.append(link) for link in list_of_links if "https://www.livelib.ru/book/" in link]
    [links_authors.append(link) for link in list_of_links if "https://www.livelib.ru/author/" in link]

links_books = list(set(links_books))
links_authors = list(set(links_authors))

print('len books: {}'.format(len(links_books)))
print('len authors: {}'.format(len(links_authors)))

with open('links_books_2.txt', 'w') as f:
    for item in links_books:
        f.write("%s\n" % item)

with open('links_authors_2.txt', 'w') as f:
    for item in links_authors:
        f.write("%s\n" % item)
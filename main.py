from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import re

def aquire_df_from_book(bc_info, bc_rating, bc_stat, bc_edition):
    pass

def parse_info(bc_info):

    pass

def parse_rating(bc_rating):
    splitted_rating = re.split("\n", re.sub(u"\xa0", '', bc_rating))
    rating = splitted_rating[0]
    return pd.DataFrame(data=[rating],
                        columns=['Rating'])

def parse_stat(bc_stat):
    splitted_stat = re.split("\n", re.sub(u"\xa0", '', bc_stat))
    have_read = splitted_stat[0]
    planned = splitted_stat[2]
    reviews = splitted_stat[4]
    quotes = splitted_stat[7]
    return pd.DataFrame(data=[have_read, planned, reviews, quotes],
                        columns=['HaveRead', 'Planned', 'Reviews', 'Quotes'])


def parse_edition(bc_edition):
    splitted_edition = re.split("\n", re.sub(u"\xa0", '', bc_edition))
    series = splitted_edition[1]
    edition = splitted_edition[3]
    pd.DataFrame(data=[series, edition],
                 columns=['Series', 'Edition'])


#url = "https://www.livelib.ru/book/1006221700-gordost-i-predubezhdenie-dzhejn-ostin"
url = "https://www.livelib.ru/book/1000031495-velikij-getsbi-frensis-skott-fitsdzherald"

req = Request(url, headers={'User-Agent': 'Mozilla/6.0'})
html = urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
bc_info = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-info')[0].get_text().strip()))

bc_rating = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-rating')[0].get_text().strip()))

bc_stat = re.sub(' +', '', re.sub('\n+', '\n', soup.select('div.bc-stat')[0].get_text().strip()))

bc_edition = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('table.bc-edition')[0].get_text().strip()))

splitted_rating = re.split("\n", re.sub(u"\xa0", '', bc_rating))
print(splitted_rating)

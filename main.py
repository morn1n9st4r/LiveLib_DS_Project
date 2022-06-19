from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re

def aquire_df_from_book(bc_info, bc_rating, bc_stat, bc_edition):
    pass

def parse_info(bc_info):
    pass

def parse_rating(bc_rating):
    pass

def parse_stat(bc_stat):
    pass

def parse_edition(bc_edition):
    pass


url = "https://www.livelib.ru/book/1006221700-gordost-i-predubezhdenie-dzhejn-ostin"
req = Request(url, headers={'User-Agent': 'Mozilla/6.0'})
html = urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
bc_info = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-info')[0].get_text().strip()))

bc_rating = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-rating')[0].get_text().strip()))

bc_stat = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-stat')[0].get_text().strip()))

bc_edition = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('table.bc-edition')[0].get_text().strip()))

print(bc_info)
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import re


# regex_name = r'(?s)(?<=Содержание).*?(?=.—.)'
# regex_author = r'(?s)(?<=.—.).*?(?=,)'


def aquire_df_from_book(h1_title, h2_author, bc_info, bc_rating, bc_stat, bc_edition):
    return pd.concat([parse_title_and_author(h1_title, h2_author),
                      parse_info(bc_info),
                      parse_rating(bc_rating),
                      parse_stat(bc_stat),
                      parse_edition(bc_edition)], axis=1)


def parse_title_and_author(h1_title, h2_author):
    data = {
        'BookTitle': [h1_title],
        'Author': [h2_author]
    }
    df = pd.DataFrame(data)

    return df


def parse_info(bc_info):
    regex_isbn = r'[-X0-9]{10,15}'
    regex_year = r'\bГод.издания: \d+'

    regex_pages_v1 = r'\bКоличество.страниц: \d+'
    regex_pages_v2 = r'\bСтраниц: \d+'
    regex_pages_v3 = r'\d+\s*стр'

    regex_books = r'\bТираж: \d+'
    regex_restrictions = r'\Возрастные.ограничения: \d+'
    regex_genres = r'(?s)(?<=Жанры:).*?(?=Теги:)'
    regex_translator = r'Перевод[чик]*[и]*: .+'

    # isbn's
    pattern = re.compile(regex_isbn, re.UNICODE)
    isbn = pattern.findall(bc_info)

    pattern = re.compile(regex_year, re.UNICODE)
    year = re.search(r"\d+", pattern.findall(bc_info)[0])

    pattern = re.compile(regex_pages_v1, re.UNICODE)
    pages = pattern.findall(bc_info)

    if not pages:
        pattern = re.compile(regex_pages_v2, re.UNICODE)
        pages = pattern.findall(bc_info)

        if not pages:
            pattern = re.compile(regex_pages_v3, re.UNICODE)
            pages = pattern.findall(bc_info)

    pages = re.search(r"\d+", ''.join(pages[0]))[0]

    pattern = re.compile(regex_books, re.UNICODE)
    copies = re.search(r"\d+", ''.join(pattern.findall(bc_info)[0]))

    pattern = re.compile(regex_restrictions, re.UNICODE)
    restrictions = re.search(r"\d+", pattern.findall(bc_info)[0])

    pattern = re.compile(regex_genres, re.UNICODE)

    genres = pattern.findall(bc_info)[0]
    genres = re.sub(u"\xa0", '', genres)
    genres = re.sub(u"\u2002", '', genres)
    genres = re.sub(u" \n ", '', genres)
    genres = re.sub(u"\n", '', genres)

    pattern = re.compile(regex_translator, re.UNICODE)
    translator = re.sub(r'Перевод[чик]*[и]*: ', '', pattern.findall(bc_info)[0])

    data = {
        'ISBN': isbn,
        'Year': [year[0]],
        'Pages': [pages],
        'Copies': [copies[0]],
        'AgeRestrictions': [restrictions[0]],
        'Genres': [''.join(genres)],
        'TranslatorName': [translator]
    }
    df = pd.DataFrame(data)

    return df


def parse_rating(bc_rating):
    splitted_rating = re.split("\n", re.sub(u"\xa0", '', bc_rating))
    rating = splitted_rating[0]

    data = {
        'Rating': [rating]
    }

    df = pd.DataFrame(data)

    return df


def parse_stat(bc_stat):
    splitted_stat = re.split("\n", re.sub(u"\xa0", '', bc_stat))
    have_read = splitted_stat[0]
    planned = splitted_stat[2]
    reviews = splitted_stat[4]
    quotes = splitted_stat[7]

    data = {
        'HaveRead': [have_read],
        'Planned': [planned],
        'Reviews': [reviews],
        'Quotes': [quotes]
    }

    df = pd.DataFrame(data)

    return df


def parse_edition(bc_edition):
    splitted_edition = re.split("\n", re.sub(u"\xa0", '', bc_edition))
    series = splitted_edition[1]
    edition = splitted_edition[3]

    data = {
        'Series': [series],
        'Edition': [edition]
    }

    df = pd.DataFrame(data)

    return df


# url = "https://www.livelib.ru/book/1006221700-gordost-i-predubezhdenie-dzhejn-ostin"
# url = "https://www.livelib.ru/book/1000483887-sorok-pyat-aleksandr-dyuma"
url = "https://www.livelib.ru/book/1000006896-bojtsovskij-klub-chak-palanik"
# url = "https://www.livelib.ru/book/1000848097-chuma-alber-kamyu"

req = Request(url, headers={'User-Agent': 'APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)'})
html = urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

h1_title = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('h1.bc__book-title')[0].get_text().strip()))

h2_author = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('h2.bc-author')[0].get_text().strip()))

bc_info = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-info')[0].get_text().strip()))

bc_rating = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-rating')[0].get_text().strip()))

bc_stat = re.sub(' +', '', re.sub('\n+', '\n', soup.select('div.bc-stat')[0].get_text().strip()))

bc_edition = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('table.bc-edition')[0].get_text().strip()))

#print(bc_info)

print(aquire_df_from_book(h1_title, h2_author, bc_info, bc_rating, bc_stat, bc_edition).to_string())

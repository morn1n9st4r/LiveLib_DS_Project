from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import re


# regex_name = r'(?s)(?<=Содержание).*?(?=.—.)'
# regex_author = r'(?s)(?<=.—.).*?(?=,)'
class BookParser:

    def __init__(self, url,
                 userAgent='APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)'):
        self.url = url
        self.userAgent = userAgent

    def scrape_text(self):
        req = Request(self.url, headers={'User-Agent': self.userAgent})
        html = urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        h1_title = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('h1.bc__book-title')[0].get_text().strip()))
        h2_author = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('h2.bc-author')[0].get_text().strip()))
        bc_info = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-info')[0].get_text().strip()))
        print(bc_info)
        bc_rating = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('div.bc-rating')[0].get_text().strip()))
        bc_stat = re.sub(' +', '', re.sub('\n+', '\n', soup.select('div.bc-stat')[0].get_text().strip()))
        bc_edition = re.sub(' +', ' ', re.sub('\n+', '\n', soup.select('table.bc-edition')[0].get_text().strip()))

        return self.aquire_df_from_book(h1_title, h2_author, bc_info, bc_rating, bc_stat, bc_edition)

    def aquire_df_from_book(self, h1_title, h2_author, bc_info, bc_rating, bc_stat, bc_edition):
        return pd.concat([self.parse_title_and_author(h1_title, h2_author),
                          self.parse_info(bc_info),
                          self.parse_rating(bc_rating),
                          self.parse_stat(bc_stat),
                          self.parse_edition(bc_edition)], axis=1)

    def parse_title_and_author(self, h1_title, h2_author):
        data = {
            'BookTitle': [h1_title],
            'Author': [h2_author]
        }
        df = pd.DataFrame(data)

        return df

    def parse_info(self, bc_info):
        regex_isbn = r'ISBN: [-X0-9]{10,15}.+'
        regex_year = r'\bГод.издания: \d+'

        regex_pages_v1 = r'\bКоличество.страниц: \d+'
        regex_pages_v2 = r'\bСтраниц: \d+'
        regex_pages_v3 = r'\d+\s*стр'

        regex_books = r'\bТираж.* \d+'
        regex_restrictions = r'\Возрастные.ограничения: \d+'
        regex_genres = r'(?s)(?<=Жанры:).*?(?=Теги:)'
        regex_translator = r'Перевод[чик]*[и]*: .+'

        # isbn's
        pattern = re.compile(regex_isbn, re.UNICODE)
        isbn = pattern.findall(bc_info)[0]

        regex_isbn_nums = r'[-X0-9]{10,15}'
        pattern = re.compile(regex_isbn_nums, re.UNICODE)
        isbn = pattern.findall(isbn)


        pattern = re.compile(regex_year, re.UNICODE)
        year = re.search(r"\d+", pattern.findall(bc_info)[0])[0]

        # pages
        # dangerous category since it could be not listed
        # need try-except clause

        pattern = re.compile(regex_pages_v1, re.UNICODE)
        pages = pattern.findall(bc_info)
        try:
            if not pages:
                pattern = re.compile(regex_pages_v2, re.UNICODE)
                pages = pattern.findall(bc_info)

                if not pages:
                    pattern = re.compile(regex_pages_v3, re.UNICODE)
                    pages = pattern.findall(bc_info)

            pages = re.search(r"\d+", ''.join(pages[0]))[0]
        except IndexError:
            pages = 'None'


        pattern = re.compile(regex_books, re.UNICODE)
        copies = pattern.findall(bc_info)

        try:
            copies = re.search(r"\d+", ''.join(copies[0]))[0]
        except IndexError:
            copies = 'None'

        pattern = re.compile(regex_restrictions, re.UNICODE)
        restrictions = re.search(r"\d+", pattern.findall(bc_info)[0])[0]

        pattern = re.compile(regex_genres, re.UNICODE)

        genres = pattern.findall(bc_info)[0]
        genres = re.sub(u"\xa0", '', genres)
        genres = re.sub(u"\u2002", '', genres)
        genres = re.sub(u" \n ", '', genres)
        genres = re.sub(u"\n", '', genres)

        pattern = re.compile(regex_translator, re.UNICODE)
        translator = pattern.findall(bc_info)
        try:
            translator = re.sub(r'Перевод[чик]*[и]*: ', '', translator[0])
        except IndexError:
            translator = 'None'

        data = {
            'ISBN': [isbn],
            'Year': [year],
            'Pages': [pages],
            'Copies': [copies],
            'AgeRestrictions': [restrictions],
            'Genres': [''.join(genres)],
            'TranslatorName': [translator]
        }
        df = pd.DataFrame(data)

        return df

    def parse_rating(self, bc_rating):
        splitted_rating = re.split("\n", re.sub(u"\xa0", '', bc_rating))
        rating = splitted_rating[0]

        data = {
            'Rating': [rating]
        }

        df = pd.DataFrame(data)

        return df

    def parse_stat(self, bc_stat):
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

    def parse_edition(self, bc_edition):
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
# url = "https://www.livelib.ru/book/1000006896-bojtsovskij-klub-chak-palanik"
# url = "https://www.livelib.ru/book/1000848097-chuma-alber-kamyu"
# url = "https://www.livelib.ru/book/1000480620-zelenaya-milya-stiven-king"
url = "https://www.livelib.ru/book/1000002563-master-i-margarita-mihail-bulgakov"


bp = BookParser(url)
print(bp.scrape_text().to_string())

# print(bc_info)



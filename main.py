from time import sleep
import pandas as pd
from BookParser import BookParser
from datetime import datetime

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#urls = ["https://www.livelib.ru/book/1006221700-gordost-i-predubezhdenie-dzhejn-ostin",
#        "https://www.livelib.ru/book/1000483887-sorok-pyat-aleksandr-dyuma",
#        "https://www.livelib.ru/book/1000006896-bojtsovskij-klub-chak-palanik",
#        "https://www.livelib.ru/book/1000848097-chuma-alber-kamyu",
#        "https://www.livelib.ru/book/1000480620-zelenaya-milya-stiven-king",
#        "https://www.livelib.ru/book/1000002563-master-i-margarita-mihail-bulgakov",
#        "https://www.livelib.ru/book/1006906093-pesn-prizrachnogo-lesa-erika-uoters",
#        "https://www.livelib.ru/book/1004112562-pervyj-zakon-krov-i-zhelezo-dzho-aberkrombi",
#        "https://www.livelib.ru/book/1000031495-velikij-getsbi-frensis-skott-fitsdzherald",
#        "https://www.livelib.ru/book/1000333658-subbota-ien-makyuen"]

urls = []

with open('links.txt') as f:
    urls = f.read().splitlines()


df = pd.DataFrame()
i = 1

for i in range(len(urls)):

    print('{} : {}'.format(i, urls[i]))

    bp = BookParser(url=urls[i])
    try:
        df_book = bp.scrape_text()
        df = df.append(df_book, ignore_index=True)
    except IndexError:
        print('\nexception at book {}\n'.format(i+1))
        continue
    sleep(1)

print(df.head(5).to_string())

df.to_csv('livelib_books.csv', encoding='utf-8-sig', index=False)
#f = codecs.open("1.html", 'r', 'utf-8')
#document = BeautifulSoup(f.read(), "html.parser")
#print(str(document))
#reg = r'a\s+[^>]*?href="([^"]*)"'
#pattern = re.compile(reg, re.UNICODE)
#list_of_links = pattern.findall(str(document))
#list_filtered = []
#[list_filtered.append(link) for link in list_of_links if "book" in link]
#print(list_filtered)

#with open('links.txt', 'w') as f:
#    for item in list_filtered:
#        f.write("%s\n" % item)

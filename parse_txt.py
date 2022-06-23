from time import sleep
import pandas as pd
from BookParser import BookParser
from datetime import datetime

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def aquire_and_save_dataframe_from_txt(filename,
                                       target="parsed_books.csv"):
    urls = []

    with open(filename) as f:
        urls = f.read().splitlines()

    df = pd.DataFrame()

    for i in range(len(urls)):

        # display № of current link and link itself
        print('{} : {}'.format(i, urls[i]))

        # sometimes parsing is stuck
        # so every 500 rows we save progress at other file
        if i % 500 == 0:
            df.to_csv(str(i) + '_' + target, encoding='utf-8-sig', index=False)

        bp = BookParser(url=urls[i])
        try:
            df_book = bp.scrape_text()
            df = df.append(df_book, ignore_index=True)

            # display added book
            print(df.tail(1).to_string())
        except IndexError:
            print('\nexception at book {}\n'.format(i + 1))
            continue

    print(df.sample(10).to_string())

    df.to_csv(target, encoding='utf-8-sig', index=False)
    return df


postfix = 6

aquire_and_save_dataframe_from_txt('links_books{}.txt'.format(postfix),
                                   'livelib_books_{}.csv'.format(postfix))

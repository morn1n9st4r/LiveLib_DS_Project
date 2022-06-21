from BookParser import BookParser


# url = "https://www.livelib.ru/book/1006221700-gordost-i-predubezhdenie-dzhejn-ostin"
# url = "https://www.livelib.ru/book/1000483887-sorok-pyat-aleksandr-dyuma"
# url = "https://www.livelib.ru/book/1000006896-bojtsovskij-klub-chak-palanik"
# url = "https://www.livelib.ru/book/1000848097-chuma-alber-kamyu"
# url = "https://www.livelib.ru/book/1000480620-zelenaya-milya-stiven-king"
# url = "https://www.livelib.ru/book/1000002563-master-i-margarita-mihail-bulgakov"
# url = "https://www.livelib.ru/book/1006906093-pesn-prizrachnogo-lesa-erika-uoters"
# url = "https://www.livelib.ru/book/1004112562-pervyj-zakon-krov-i-zhelezo-dzho-aberkrombi"
url = "https://www.livelib.ru/book/1000031495-velikij-getsbi-frensis-skott-fitsdzherald"

bp = BookParser(url=url)
print(bp.scrape_text().to_string())

import re

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]


def recursion(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawPage = web_byte.decode('utf-8')
    soup = BeautifulSoup(rawPage, 'html.parser')
    for tag in soup.find_all("div", class_="c-postList__post__thumbnail"):

        # FOR EACH ARTICLE ON RESULTS PAGE
        for link in tag.find_all('a'):
            print(link.get('href'))
            url = link.get('href')
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            web_byte = urlopen(req).read()
            rawPage = web_byte.decode('utf-8')
            article = BeautifulSoup(rawPage, 'html.parser')

            # GETS THE TEXT OF A SINGLE ARTICLE
            for text in article.find_all("p"):
                # since each line is scanned in this is a bit redundancy
                # also might be removing some article if in last line
                str = remove_last_line_from_string(text.get_text().replace('jsaltz@villagevoice.com', ''))
                if len(str) != 0:
                    print(str)

    for t in soup.find_all("a", class_="next page-numbers"):
        if len(t) == 1:
            return recursion(t.get('href'))
        else:
            return


url = 'https://www.villagevoice.com/author/jerrysaltz/page/34/'
recursion(url)


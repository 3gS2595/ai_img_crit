from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# Recursive method iterating through
# VillageVoice.com articles written by Saltz
def nextPage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode('utf-8')
    soup = BeautifulSoup(rawhtml, 'html.parser')
    for tag in soup.find_all("div", class_="c-postList__post__title c-postList__post__title__wo_dek"):
        # FOR EACH ARTICLE ON RESULTS PAGE
        for link in tag.find_all('a'):
            print(link.get('href'))
            url = link.get('href')
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            web_byte = urlopen(req).read()
            rawhtml = web_byte.decode('utf-8')
            article = BeautifulSoup(rawhtml, 'html.parser')

            # GETS THE TEXT OF A SINGLE ARTICLE
            for text in article.find_all("p"):
                # since each line is scanned in this is a bit redundancy
                # also might be removing some article if in last line
                str = text.get_text()
                if len(str) != 0 and not ('More:' in str) and not ('jsaltz@villagevoice.com' in str):
                    print(str)

    for t in soup.find_all("a", class_="next page-numbers"):
        if len(t) == 1:
            return nextPage(t.get('href'))
        else:
            return


entryPoint = 'https://www.villagevoice.com/author/jerrysaltz/'
nextPage(entryPoint)

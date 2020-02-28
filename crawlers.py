from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# returns URL's HTML
def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode('utf-8')
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup


# Recursive method iterating through
# VillageVoice.com articles written by Saltz
def VillVoice(url):
    soup = getHTML(url)
    for tag in soup.find_all("div", class_="c-postList__post__title c-postList__post__title__wo_dek"):

        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            url = link.get('href')
            article = getHTML(url)

            # GRABS TEXT OF A SINGLE ARTICLE
            for text in article.find_all("p"):
                str = text.get_text()
                if len(str) != 0 and not ('More:' in str) and not ('jsaltz@villagevoice.com' in str):
                    print(str)

    # GRABS THE NEXT RESULTS PAGE URL
    for t in soup.find_all("a", class_="next page-numbers"):
        if len(t) != 0:
            return VillVoice(t.get('href'))
        else:
            return


start = 'https://www.villagevoice.com/author/jerrysaltz/'
VillVoice(start)

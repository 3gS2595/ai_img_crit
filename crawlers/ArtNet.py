from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# Returns URL's HTML
def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode("latin-1")
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup


# finds all artnet.com Saltz articles URL
def ArtNetCrawler(url0, cnt, fin):
    soup = getHTML(url0)
    for tag in soup.find_all("div", class_="text"):

        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            cnt = cnt + 1
            url = link.get('href')

            # SENDS URL TO EXTRACTOR
            fin = fin + ArtNetExtractor(url)
            print("{}\nfin: {} cnt: {}\n\n ".format(url, fin, cnt, ))


# using artnet.com URL extracts article text
def ArtNetExtractor(url):
    # GRABS TEXT OF A SINGLE ARTICLE
    flag = 0
    article = getHTML('http://www.artnet.com' + url)
    for text in article.find_all("p"):
        text = text.get_text()
        if len(text) != 0 and not ('JERRY SALTZ is' in text
                                   or 'daily newsletter' in text
                                   or 'Artnet Worldwide' in text
                                   or 'subscribing!' in text):
            if flag == 0:
                flag = 1

            # EXTRACTED ARTICLE TEXT
            # print(text)
    return flag


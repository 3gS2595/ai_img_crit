from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from crawlers.tools import nameDict


# finds all artnet.com Saltz articles URL
def ArtNetCrawler(url0, dic):
    print(url0)
    soup = getHTML(url0)
    for tag in soup.find_all("div", class_="text"):

        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            dic['numURL'] = dic.get('numURL') + 1

            # SENDS URL TO EXTRACTOR
            url = link.get('href')
            ArtNetExtractor(url, dic)

            # PRINTS TOTAL NAMES, ARTICLES PROCESSED
            print("len: {} cnt: {}".format((len(dic) - 1), dic.get('numURL')))


# using artnet.com URL extracts article text
def ArtNetExtractor(url, dic):
    out = ""
    article = getHTML(url)
    for text in article.find_all("p"):
        text = text.get_text()
        if len(text) != 0 and not ('JERRY SALTZ is' in text
                                   or 'daily newsletter' in text
                                   or 'Jerry Saltz' in text
                                   or 'Artnet Worldwide' in text
                                   or 'subscribing!' in text):
            # EXTRACTED ARTICLE TEXT
            out = out + text

    # PARSES AND EXTRACTS SENTENCES WITH NAMES
    # PLACES IN DICT (KEY=NAME, VALUE=COUNTER)
    nameDict(dic, out)


# Returns URL's HTML
def getHTML(url):
    req = Request(('http://www.artnet.com' + url), headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode("latin-1")
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup

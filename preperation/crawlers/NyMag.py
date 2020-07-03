from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from crawlers.tools import nameDict, printOut


# finds all artnet.com Saltz articles URL
def NyMagCrawler(url0, dic, limit):
    soup = getHTML(url0)
    for tag in soup.find_all('div', class_='container-main'):

        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            if dic.get('numURL') >= limit:
                return
            dic['numURL'] = dic.get('numURL') + 1
            # EXTRACTS LINKS
            url = link.get('href')
            url = url[-(len(url) - 2):]
            # CHECKS IF LINK ROUTES TO NEXT RESULTS PAGE
            if 'tart=' in url:
                NyMagCrawler('https://nymag.com/author/jerry-saltz/?s' + url, dic, limit)
            else:
                # SENDS URL TO EXTRACTOR
                NyMagExtractor('https://' + url, dic)

                # PRINTS TOTAL NAMES, ARTICLES PROCESSED
                printOut(dic, url)


# using artnet.com URL extracts article text
def NyMagExtractor(url, dic):
    out = ""
    article = getHTML(url)
    for text in article.find_all('p'):
        text = text.get_text()
        if len(text) != 0 and not ('to see selections' in text
                                   or 'a subscriber?' in text
                                   or 'Terms of Use' in text
                                   or 'Jerry Saltz' in text
                                   or 'days in the art world with Seen.' in text
                                   or 'Sign up here to get it nightly.' in text
                                   or 'magazine subscription' in text
                                   or 'Subscribe Now!' in text):
            # EXTRACTED ARTICLE TEXT
            out = out + text

    # PARSES AND EXTRACTS SENTENCES WITH NAMES
    # PLACES IN DICT (KEY=NAME, VALUE=COUNTER)
    dic['articles'].append(out)


# Returns URL's HTML
def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode('utf-8')
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup

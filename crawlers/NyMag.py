from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# Returns URL's HTML
def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode('utf-8')
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup


# finds all artnet.com Saltz articles URL
def NyMagCrawler(url0, cnt, fin):
    out = ""
    soup = getHTML(url0)
    for tag in soup.find_all('div', class_='container-main'):
        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            cnt = cnt + 1
            url = link.get('href')
            url = url[-(len(url) - 2):]
            if 'tart=' in url:
                NyMagCrawler('https://nymag.com/author/jerry-saltz/?s' + url, cnt, fin)
            else:
                output = out + NyMagExtractor('https://' + url)
                print("len: {} cnt: {}".format(len(output), cnt))
            # SENDS URL TO EXTRACTOR

    return out

# using artnet.com URL extracts article text
def NyMagExtractor(url):
    output = ""
    article = getHTML(url)
    for text in article.find_all('p'):
        text = text.get_text()
        if len(text) != 0 and not ('to see selections' in text
                                   or 'a subscriber?' in text
                                   or 'Terms of Use' in text
                                   or 'magazine subscription' in text
                                   or 'Subscribe Now!' in text):
            # EXTRACTED ARTICLE TEXT
            output = output + text
    return output
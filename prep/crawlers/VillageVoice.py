from urllib.request import Request, urlopen
from prep.crawlers.tools import nameDict, printOut
from bs4 import BeautifulSoup


# Recursive method iterating through
# VillageVoice.com articles written by Saltz

def VillageVoiceCrawler(url, dic, limit):
    soup = getHTML(url)
    for tag in soup.find_all("div", class_="c-postList__post__title c-postList__post__title__wo_dek"):

        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            if dic.get('numURL') >= limit:
                return
            printOut(dic, url)
            dic['numURL'] = dic.get('numURL') + 1
            # SENDS URL TO EXTRACTOR
            url = link.get('href')
            if 'jerrysaltz/page/' not in url:
                VillageVoiceExtractor(url, dic)

    # GRABS THE NEXT RESULTS PAGE URL
    for t in soup.find_all("a", class_="next page-numbers"):
        if len(t) != 0:
            return VillageVoiceCrawler(t.get('href'), dic, limit)
        else:
            return


# using villagevoice.com URL extracts article text
def VillageVoiceExtractor(url, dic):
    out = ""
    article = getHTML(url)
    for rawText in article.find_all("p"):
        text = rawText.get_text()
        if len(text) != 0 and not ('More:' in text) and not ('jsaltz@villagevoice.com' in text):
            # EXTRACTED ARTICLE TEXT
            out = out + text
    dic['articles'].append(out)


def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode("utf-8")
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup

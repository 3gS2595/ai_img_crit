from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# Returns URL's HTML
def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    rawhtml = web_byte.decode("utf-8")
    soup = BeautifulSoup(rawhtml, 'html.parser')
    return soup


# Recursive method iterating through
# VillageVoice.com articles written by Saltz
def VillageVoiceCrawler(url, cnt, fin):
    soup = getHTML(url)
    for tag in soup.find_all("div", class_="c-postList__post__title c-postList__post__title__wo_dek"):

        # ITERATES THROUGH ARTICLES ON RESULTS PAGE
        for link in tag.find_all('a'):
            cnt = cnt + 1
            url = link.get('href')
            fin = fin + VillageVoiceExtractor(url)
            print("fin: {} cnt: {}".format(fin, cnt))

    # GRABS THE NEXT RESULTS PAGE URL
    for t in soup.find_all("a", class_="next page-numbers"):
        if len(t) != 0:
            return VillageVoiceCrawler(t.get('href'), cnt, fin)
        else:
            return cnt


# using villagevoice.com URL extracts article text
def VillageVoiceExtractor(url):
    flag = 0
    article = getHTML(url)
    for rawText in article.find_all("p"):
        text = rawText.get_text()
        if len(text) != 0 and not ('More:' in text) and not ('jsaltz@villagevoice.com' in text):
            if flag == 0:
                flag = 1

            # EXTRACTED ARTICLE TEXT
            # print(text)

    return flag


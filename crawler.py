import sys

from crawlers.NyMag import NyMagCrawler
from crawlers.ArtNet import ArtNetCrawler
from crawlers.VillageVoice import VillageVoiceCrawler
from crawlers.tools import analysis, saveArticles
from generateJSON import generateJSON
from crawlers.imageGrab import grab


# ARTICLE COUNTER
dic = {'numURL': 0, 'articles': []}
txt = input("crawl articles?---(\'y\' or \'n\') : ")
if txt == 'y':

    # for debugging
    articleLimit = sys.maxsize

    start = "https://www.villagevoice.com/author/jerrysaltz/"
    VillageVoiceCrawler(start, dic, articleLimit)

    start = "https://nymag.com/author/jerry-saltz/"
    NyMagCrawler(start, dic, articleLimit)

    start = "/magazineus/authors/saltz.asp"
    ArtNetCrawler(start, dic, articleLimit)

    saveArticles(dic)

# minimum limit of available sentences
limit = 5
txt = input("analyze articles?-(\'y\' or \'n\') : ")
if txt == 'y':
    # counts how many times names are mentioned
    dic = analysis(dic, limit)

# number of images to grab
limit = 5
txt = input("crawl images?-----(\'y\' or \'n\') : ")
if txt == 'y':
    grab(limit)

# number of sentences included in JSON
limit = 5
generateJSON(limit)



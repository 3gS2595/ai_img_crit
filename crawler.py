from crawlers.NyMag import NyMagCrawler
from crawlers.ArtNet import ArtNetCrawler
from crawlers.VillageVoice import VillageVoiceCrawler
from operator import itemgetter


def top(dic):
    high = 0
    for k, v in sorted(dic.items(), key=itemgetter(1)):
        if v > high:
            high = v
    for k, v in sorted(dic.items(), key=itemgetter(1)):
        if v >= (high - 30):
            print(v, k)


# found urls
dic = {'numURL': 0}

start0 = "/magazineus/authors/saltz.asp"
ArtNetCrawler(start0, dic)
top(dic)

start0 = "https://www.villagevoice.com/author/jerrysaltz/"
VillageVoiceCrawler(start0, dic)
top(dic)

start0 = "https://nymag.com/author/jerry-saltz/"
NyMagCrawler(start0, dic)
top(dic)

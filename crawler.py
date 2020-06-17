from crawlers.NyMag import NyMagCrawler
from crawlers.ArtNet import ArtNetCrawler
from crawlers.VillageVoice import VillageVoiceCrawler
from crawlers.tools import top
from generateJSON import generateJSON


# ARTICLE COUNTER
dic = {'numURL': 0}

start = "https://www.villagevoice.com/author/jerrysaltz/"
VillageVoiceCrawler(start, dic)

start = "https://nymag.com/author/jerry-saltz/"
NyMagCrawler(start, dic)

start = "/magazineus/authors/saltz.asp"
ArtNetCrawler(start, dic)

top(dic)
generateJSON()
print('finished')

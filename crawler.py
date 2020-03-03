from crawlers.ArtNet import ArtNetCrawler
from crawlers.NyMag import NyMagCrawler
from crawlers.VillageVoice import VillageVoiceCrawler

# found urls
numURL = 0
# successfully scraped
numFIN = 0

start0 = "https://nymag.com/author/jerry-saltz/"
NyMagCrawler(start0, numURL, numFIN)

start0 = "https://www.villagevoice.com/author/jerrysaltz/"
VillageVoiceCrawler(start0, numURL, numFIN)

start0 = "http://www.artnet.com/magazineus/authors/saltz.asp"
ArtNetCrawler(start0, numURL, numFIN)



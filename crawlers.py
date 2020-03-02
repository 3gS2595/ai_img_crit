from crawlers.VillageVoice import VillageVoiceCrawler
from crawlers.ArtNet import ArtNetCrawler

# found urls
numURL = 0
# successfully scraped
numFIN = 0

start0 = "https://www.villagevoice.com/author/jerrysaltz/"
# VillageVoiceCrawler(start0, numURL, numFIN)

start0 = "http://www.artnet.com/magazineus/authors/saltz.asp"
ArtNetCrawler(start0, numURL, numFIN)

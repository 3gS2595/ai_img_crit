from crawlers.NyMag import NyMagCrawler
from crawlers.ArtNet import ArtNetCrawler
from crawlers.VillageVoice import VillageVoiceCrawler

# found urls
numURL = 0
# successfully scraped
numFIN = 0

text_file = open("output.txt", "wt")
output = ""

start0 = "/magazineus/authors/saltz.asp"
output = output + ArtNetCrawler(start0, numURL)
n = text_file.write(output)

start0 = "https://www.villagevoice.com/author/jerrysaltz/"
output = output + VillageVoiceCrawler(start0, numURL, numFIN, "")
n = text_file.write(output)

start0 = "https://nymag.com/author/jerry-saltz/"
output = output + NyMagCrawler(start0, numURL, numFIN)
n = text_file.write(output)

text_file.close()




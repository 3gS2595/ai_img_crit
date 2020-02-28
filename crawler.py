from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


html_doc = " "
with open('village.html', 'r') as file:
    html_doc = file.read().replace('\n', '')

soup = BeautifulSoup(html_doc, 'html.parser')
temp = soup.find_all("div", class_="c-postList__post__thumbnail")

for tag in soup.find_all("div", class_="c-postList__post__thumbnail"):
    for link in tag.find_all('a'):
        print(link.get('href'))
        url = link.get('href')
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')
        print(req.text)




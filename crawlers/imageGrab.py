import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import time

urllib3.disable_warnings(InsecureRequestWarning)
maxcount = 30
chromedriver = '/home/clem/chromedriver'


def download_google_staticimages(searchurl, dirs):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    print(f'Getting you a lot of images. This may take a few moments...')

    element = browser.find_element_by_tag_name('body')

    # Scroll down
    # for i in range(30):
    for i in range(5):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    time.sleep(0.5)
    time.sleep(0.5)

    #

    # elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
    # page_source = elements[0].get_attribute('innerHTML')
    page_source = browser.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    images = soup.find_all('img')

    cn = 0
    urls = []
    for image in images:
        if cn < maxcount:
            try:
                url = image['data-src']
                if not url.find('https://'):
                    urls.append(url)
                    cn = cn + 1
            except:
                try:
                    url = image['src']
                    if not url.find('https://'):
                        urls.append(image['src'])
                        cn = cn + 1
                except Exception as e:
                    print(f'No found image sources.')
                    print(e)

    count = 0
    if urls:
        for url in urls:
            if count <= maxcount:
                try:
                    res = requests.get(url, verify=False, stream=True)
                    rawdata = res.raw.read()
                    with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                        f.write(rawdata)
                        count += 1
                except Exception as e:
                    print('Failed to write rawdata.')
                    print(e)

    browser.close()
    return count


# Main block
def grab(first, last):
    word1 = first
    word2 = last
    searchurl = 'https://www.google.com/search?q=' + 'art+done+by+' + word1 + '+' + word2 + '&source=lnms&tbm=isch'

    dirs = 'data/' + first + last
    if not os.path.exists(dirs):
        os.mkdir(dirs)

    t0 = time.time()
    count = download_google_staticimages(searchurl, dirs)
    t1 = time.time()

    total_time = t1 - t0
    print(f'Download completed. [Successful count = {count}].')
    print(f'Total time is {str(total_time)} seconds.')

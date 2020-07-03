import os
import sys
import time

import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
chromedriver = '/home/clem/chromedriver'


def download_google_staticimages(searchurl, dirs, limit, browser):
    browser.get(searchurl)
    element = browser.find_element_by_tag_name('body')

    # Scroll down
    # for i in range(30):
    for i in range(2):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(4):
            element.send_keys(Keys.PAGE_DOWN)
            # time.sleep(0.1)
    except:
        for i in range(2):
            element.send_keys(Keys.PAGE_DOWN)
            # time.sleep(0.3)

    # elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
    # page_source = elements[0].get_attribute('innerHTML')
    page_source = browser.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    images = soup.find_all('img')

    cn = 0
    urls = []
    for image in images:
        if cn < limit:
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
            if count <= limit:
                try:
                    res = requests.get(url, verify=False, stream=True)
                    rawdata = res.raw.read()
                    with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                        f.write(rawdata)
                        count += 1
                except Exception as e:
                    print('Failed to write rawdata.')
                    print(e)
    return count


# Main block
def grab(limit):
    print('------------------------------')
    print('STARTING IMAGE WEB CRAWL')
    print()
    t0 = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()
    browser.set_window_size(1280, 1024)

    count = 0
    with open('./output/TOP_NAMES.txt', 'r') as fp:
        for line in fp:
            count = count + 1

    with tqdm(total=count) as pbar3:
        with open('./output/TOP_NAMES.txt', 'r') as fp:
            for line in fp:
                name = line.split()
                firstName = name[1]
                lastName = name[2]
                pbar3.set_description(desc='{} {}'.format(firstName, lastName), refresh=True)
                searchurl = 'https://www.google.com/search?q=' + 'art+done+by+' + firstName + '+' + lastName + '&source=lnms&tbm=isch'

                dirs = 'data/' + firstName + lastName
                if not os.path.exists(dirs):
                    os.mkdir(dirs)
                    print('creating directory... that is .... interesting .... ummmmm {} {}'.format(firstName,lastName))

                download_google_staticimages(searchurl, dirs, limit, browser)
                pbar3.update(1)
        pbar3.close()

    browser.close()
    print()
    t1 = time.time()
    total_time = (t1 - t0) / 60
    print(f'analysis completed in {str(round(total_time, 5))} minutes.')

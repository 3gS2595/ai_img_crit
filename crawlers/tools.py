import re
import spacy
import os
import json
import time
from tqdm import tqdm
from crawlers.imageGrab import grab


# FINDS / STORES MOST COMMON NAMES
def analysis(dic, limit):
    print('------------------------------')
    print('STARTING ANALYSIS')
    print()

    # populates dic with names and the number of mentions
    nlp = spacy.load('en_core_web_sm')
    filepath = './output/articles.txt'
    fileSize = os.path.getsize(filepath)
    t0 = time.time()
    with tqdm(total=fileSize, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        with open(filepath, 'r') as fp:
            for line in fp:
                nameDict(dic, nlp, line)
                pbar.update(len(line))
        pbar.close()
    time.sleep(1)

    path = "./output/TOP_NAMES.txt"
    f = open(path, "w+")
    for k, v in sorted(dic.items()):
        if isinstance(v, list):
            if k is not 'articles':
                if v[0] >= limit and k is not 'numURL':
                    f.write("{}".format(v[0]) + " " + k + "\n")
                else:
                    del dic[k]
    f.close()

    print()
    t1 = time.time()
    total_time = (t1 - t0) / 60
    print(f'analysis completed in {str(round(total_time, 5))} minutes.')
    createDataDirectories(dic, limit)


# PARSES AND EXTRACTS SENTENCES WITH NAMES
# PLACES IN DICT (KEY=NAME, VALUE=COUNTER)
def nameDict(dic, nlp, out):
    sentence = split_into_sentences(out)
    for sent in sentence:
        s = sent.casefold()
        if not ('booth' in s or 'fair' in s or 'gallery' in s):
            doc = nlp(sent)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    name = ent.text.replace('\'s', '')
                    if len(name.split()) >= 2:
                        if name in dic:
                            num = dic.get(name)
                            if sent not in num:
                                num[0] = num[0] + 1
                                num.append(sent)
                                dic[name] = num
                                # print(len(dic))
                                # print('{} {}'.format(num[0], name))
                        else:
                            array = [1, sent]
                            dic[name] = array


# CREATES ALL DIRECTORIES FOR EACH ARTIST
# AND PLACES IN THE SENTENCES.TXT FILE
def createDataDirectories(dic, limit):
    print('------------------------------')
    print('STARTING DIRECTORY GENERATION')
    print()

    # moves through all dic entries and creates folders
    t0 = time.time()
    with tqdm(total=len(dic)-2) as pbar2:
        for k, v in sorted(dic.items()):
            if isinstance(v, list):
                if k is not 'articles':
                    if v[0] >= limit and k is not 'numURL':

                        # creates folder for artists images and sentences
                        name = k.split(" ")
                        pathName = name[0] + name[1]
                        pbar2.set_description(desc='{} {}'.format(name[0], name[1]), refresh=True)

                        # print('creating ./data/{}'.format(pathName))
                        if not os.path.exists('./data/'):
                            os.mkdir('./data/')
                        if not os.path.exists('./data/' + pathName):
                            os.mkdir('./data/' + pathName)

                        # creates/writes too text file for sentences
                        path = "./data/" + pathName
                        if not os.path.exists(path):
                            os.mkdir(path)
                        f = open(path + "/sentences.txt", "w+")
                        for i in dic[k]:
                            if isinstance(i, str):
                                f.write(i + "\n")
                        f.close()

                        # grabs / populates folder with images
                        pbar2.update(1)
        pbar2.close()

    print()
    t1 = time.time()
    total_time = (t1 - t0) / 60
    print(f'directories created in {str(round(total_time, 5))} minutes.')


def imageGrab():
    print()
    # TODO MAKE IMAGE GRAB OPERATE BASED ON TOP_NAMES.txt


# WRITES EVERY ARTICLE FOUND BY CRAWLERS
# (FROM DIC) INTO ARTICLES.TXT
def saveArticles(dic):
    print('creating articles.txt')
    path = "./output/articles.txt"
    f = open(path, "w+")
    cnt = 0
    for i in dic['articles']:
        if len(i) > 5:
            i = i.replace('\n', '')
            f.write(i + '\n')
            cnt = cnt + 1

    print('{} present'.format(cnt))
    print('articles.txt created')
    print()


def format_bytes(size):
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n] + 'bytes'


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        print(e)
        return False
    return True


def printOut(dic, url):
    print("{}: {}".format(dic.get('numURL'), url))


def split_into_sentences(text):
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = '(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)'
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"

    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = " ".join(text.split())
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

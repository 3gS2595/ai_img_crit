import re
import spacy
import os
import json
from crawlers.imageGrab import grab


# PRINTS MOST COMMON NAMES
def top(dic):
    high = 3
    path = "./output/TOP_NAMES.txt"
    f = open(path, "w+")
    for k, v in sorted(dic.items()):
        if isinstance(v, list):
            if v[0] >= high and k is not 'numURL':
                print("{} ".format(v[0]) + k)
                f.write("{}".format(v[0]) + " " + k + "\n")
    print()

    for k, v in sorted(dic.items()):
        if isinstance(v, list):
            if v[0] >= high and k is not 'numURL':
                print(v[0], k)
                # creates folder for artists images and sentences
                name = k.split(" ")
                if not os.path.exists('./data1/' + name[0] + name[1]):
                    os.mkdir('./data1/' + name[0] + name[1])

                # places in images
                grab(name[0], name[1])

                # creates/writes too text file for sentences
                print('creating text file containing sentences')
                path = "./data1/" + name[0] + name[1]
                if not os.path.exists(path):
                    os.mkdir(path)
                f = open(path + "/sentences.txt", "w+")
                for i in dic[k]:
                    if isinstance(i, str):
                        f.write(i + "\n")
                print('sentence wrtitten for: ' + name[0] + ' ' + name[1])
                print()
        else:
            print(v)


# PARSES AND EXTRACTS SENTENCES WITH NAMES
# PLACES IN DICT (KEY=NAME, VALUE=COUNTER)
def nameDict(dic, out):
    nlp = spacy.load('en_core_web_sm')
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
                        else:
                            array = [1, sent]
                            dic[name] = array


def printOut(dic, url):
    print("peopleCnt: {} articleCnt: {}".format((len(dic) - 1), dic.get('numURL')))
    print(url)


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'


def split_into_sentences(text):
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"

    text = " " + text + "  "
    text = text.replace("\n", " ")
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


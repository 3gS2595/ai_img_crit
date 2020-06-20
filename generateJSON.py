from crawlers.tools import format_bytes, is_json
import os
import json


def generateJSON():
    json_data = {'images': []}
    images = []
    sent = []
    sentID = 0
    imgID = 0

    print('creating JSON')
    rootDir = './data'

    # iterates through the ./data directory
    for root, dirs, files in os.walk(rootDir):
        dirs.sort()
        print(root)
        for f in files:
            # scans the file directory and gathers data for JSON
            # finds sentences
            if f == 'sentences.txt':
                sent = []
                with open(root + "/" + f) as file:
                    for l in file:
                        sent.append(l.strip())
            # finds images
            else:
                # finds image file names
                if f.find('.') is not -1:
                    images.append(f)

            # place data in dic which will become the JSON
            if f != 'sentences.txt' and len(sent) > 10:

                # adds general information
                img = {}
                img['imgid'] = imgID
                img['filename'] = f
                img['filepath'] = root
                img['split'] = "train"

                # adds sentence information
                img['sentids'] = []
                img['sentences'] = []
                c = sentID
                for s in sent:
                    # creates single sentences data
                    tokens = []
                    for w in s.split(" "):
                        tokens.append(w)
                    sentGroup = {}
                    sentGroup['tokens'] = tokens
                    sentGroup['raw'] = s
                    sentGroup['imgid'] = imgID
                    sentGroup['sentid'] = c

                    # places sentence in images group
                    img['sentids'].append(c)
                    img['sentences'].append(sentGroup)
                    # print('append {} {} ID:{}'.format(f, root, c))
                    c = c + 1
                sentID = c
                imgID = imgID + 1
                json_data['images'].append(img)

    # writes/dumps to the json file
    print('-----------------------------------------------')
    print('JSON validity: {}'.format(is_json(json.dumps(json_data))))
    print('writing to file')
    path = "./JSON.json"
    with open(path, 'w') as fp:
        json.dump(json_data, fp)
    print('JSON created ({})'.format(format_bytes(os.path.getsize('./JSON.json'))))
    print('-----------------------------------------------')

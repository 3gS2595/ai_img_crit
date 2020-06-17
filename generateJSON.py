import os


def generateJSON():
    json = "{\"images\": ["
    folder = ""
    images = []
    sent = []
    sentID = 0
    imgID = 0

    rootdir = '/home/clem/PycharmProjects/TheSaltzWaltz/crawlers/data'
    for dirs in os.walk(rootdir):
        for file in dirs:
            for f in file:
                # finds sentences
                if f == 'sentences.txt':
                    sent = []
                    with open(folder + "/" + f) as file:
                        for l in file:
                            sent.append(l.strip())
                else:
                    # finds image file names
                    if f.find('.') is not -1:
                        images.append(f)

                    else:
                        # finds artist/folder name
                        if len(f) > 1:
                            folder = rootdir + "/" + f
        print(len(sent))
        print('hit')
        if len(images) > 1:
            for i in images:
                json = json + "{\"filepath\": \"" + folder + ", "

                c = 0
                json = json + "\"sentids\": ["
                for s in sent:
                    json = json + "{}".format(sentID + c) + ", "
                    c = c + 1
                json = json[:-2] + "], "

                json = json + "\"filename\": \"" + i + "\", "

                json = json + "\"imgid\": " + "{}".format(imgID) + ", "

                c = 0
                json = json + "\"sentences\": ["
                for s in sent:
                    json = json + "{\"tokens\": ["
                    for w in s.split(" "):
                        json = json + "\"" + w + "\", "
                    json = json[:-2] + "], \"raw\": \"" + s + "\", "
                    json = json + "\"imgid\": " + "{}".format(imgID) + ", "
                    json = json + "\"sentid\": " + "{}".format(sentID + c) + "}], "
                    c = c + 1

                json = json + "\"split\": \"train\"}, "

                imgID = imgID + 1
            json = json[:-2] + "]}"
            path = "./JSON"
            f = open(path, "w+")
            f.write(json)

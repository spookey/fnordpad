# -.- coding: UTF-8 -.-

import os, md5, hashlib, pprint
from random import choice
from config import staticdir, p_unsorted, p_public, p_reject, staticdir
from PIL import Image
from time import strftime

def imagelist(folder):
    result = []
    for files in os.listdir(folder):
        if files.endswith('.png') or files.endswith('.gif') or files.endswith('.jpg') or files.endswith('.jpeg'):
            if os.path.getsize(os.path.join(folder, files)) > 0:
                result.append(files)
    return result

def pathimagelist(folder):
    return ['bilder/%s/%s' %(os.path.split(folder)[1], element) for element in imagelist(folder)]

def getrandomimage(folder):
    if imagelist(folder):
        return 'bilder/%s/%s' %(os.path.split(folder)[1], choice(imagelist(folder)))
    else:
        return 'bilder/%s/fnordpad.jpg' %(os.path.split(p_public)[1])

def getnamedimage(folder, name):
    print folder, name
    if name in imagelist(folder):
        return 'bilder/%s/%s' %(os.path.split(folder)[1], name)
    else:
        return 'bilder/%s/fnordpad.jpg' %(os.path.split(p_public)[1])

def listnamedups():
    lists = imagelist(p_unsorted) +  imagelist(p_public) + imagelist(p_reject)
    allimages = [element.split('/')[-1].split('.')[0] for element in lists]
    return sorted(set([element for element in allimages if allimages.count(element) > 1]))

def snapnamedups(extension):
    folders = [os.path.split(element)[1] for element in [p_unsorted, p_public, p_reject]]
    for folder in folders:
        for element in listnamedups():
            image = '%sbilder/%s/%s.%s' %(staticdir, folder, element, extension)
            if os.path.exists(image):
                os.remove(image)

def listfiledups():
    hashmap = {}
    for path, dirs, files in os.walk(os.path.join(staticdir, 'bilder/')):
        for filename in files:
            fullname = os.path.join(path, filename)
            with open(fullname) as f:
                d = f.read()
            h = hashlib.md5(d).hexdigest()
            filelist = hashmap.setdefault(h, [])
            filelist.append(fullname)

    return pprint.pprint(hashmap)

def getbg(image):
    try:
        print 'getbg(%s)' %(image)
        img = Image.open(image)
        colors = img.getcolors(16777216)
        max_occurence, most_present = 0, 0
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except (TypeError, IOError, IndexError):
        print 'error: getbg(%s)' %(image)

def datum():
    return strftime('%d. %b %Y')

def uhr():
    return strftime('%H:%M')

def scrape(url):
    import urllib2
    response = urllib2.urlopen(url)
    return response.read()

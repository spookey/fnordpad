# -.- coding: UTF-8 -.-

import os, md5, hashlib
from time import time, strftime
from random import sample, choice
from flask import flash
from config import p_folder, p_unsorted, p_public, p_reject, i_default

def list_images(folder=None):
    if not folder:
        folder = p_unsorted
    if os.path.exists(folder):
        result = []
        for filename in os.listdir(folder):
            if any(filename.endswith(x) for x in ('jpeg', 'jpg', 'gif', 'png')):
                if os.path.getsize(os.path.join(folder, filename)) > 0:
                    result.append(filename)
        return result

# crawler
def list_all_images():
    return [item for sublist in [list_images(x) for x in (p_unsorted, p_public, p_reject)] for item in sublist]

def find_image_path(image):
    for path, dirs, files in os.walk(p_folder):
        if image in files:
            return path
    return p_folder

def zapp_image(image):
    def get_dlist():
        dups = []
        for v in filedups():
            for x in v['files']:
                if len(x) > 1:
                    dups.append(os.path.join(p_folder, x[0], x[1]))
        return dups

    if image == 'all':
        for v in get_dlist():
            zapp_image(v)
    else:
        if os.path.exists(os.path.join(find_image_path(image), image)):
            img = os.path.join(find_image_path(image), image)
            if img in get_dlist():
                print 'zapp: %s' %(img)
                flash('zapp: %s' %(str(img.split('/')[-2:])))
                os.remove(img)


def get_batch_of_images():
    l = list_images(p_public)
    try:
        n = 23 if len(l) > 23 else len(l)
        return sample(l, n)
    except TypeError:
        pass

def get_sort_image():
    l = list_images(p_unsorted)
    if len(l) > 1:
        return choice(l)
    else:
        pass

def move_image(request):
    if request['image'] in list_images(p_unsorted):
        if 'plus' in request:
            flash('plus: %s' %(request['image']))
            os.rename(os.path.join(p_unsorted, request['image']), os.path.join(p_public, request['image']))
        if 'minus' in request:
            flash('minus: %s' %(request['image']))
            os.rename(os.path.join(p_unsorted, request['image']), os.path.join(p_reject, request['image']))


def list_filedups():
    hashmap = {}
    for path, dirs, files in os.walk(p_folder):
        for filename in files:
            fullname = os.path.join(path, filename)
            with open(fullname) as f:
                d = f.read()
            h = hashlib.md5(d).hexdigest()
            filelist = hashmap.setdefault(h, [])
            filelist.append(fullname)
    return hashmap

def filedups():
    result = []
    for md5_sum, dups in list_filedups().iteritems():
        if len(dups) > 1:
            result.append({'hash': md5_sum, 'len': len(dups), 'files': [d.split('/')[-2:] for d in dups], 'thumb': dups[-1].split('/')[-1]})
    return result

def uhr():
    return strftime('%H:%M')

def datum():
    return strftime('%d. %b %Y')

def timestamp_now():
    return int(time())

def scrape(url):
    import urllib2
    try:
        response = urllib2.urlopen(url)
        print '+scrape'
        return response.read()
    except Exception, e:
        print '-scrape: %s' %(e)
        return 'error'

def json_status():
    import json
    try:
        pull = json.loads(scrape('http://status.cccmz.de/raw'))
        print '+json'
        return pull
    except Exception, e:
        print '-json: %s' %(e)
        return 'error'




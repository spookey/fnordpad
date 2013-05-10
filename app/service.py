# -.- coding: UTF-8 -.-

import os, md5, hashlib
from random import sample, choice
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
    for path in (p_reject, p_unsorted, p_public):
        print path
        if os.path.exists(os.path.join(path, image)):
            if os.path.join(path, image) in list_filedups():
                os.remove(os.path.join(path, image))
                print '\n\n\nzapp:', image, '\n'
                break;

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


    return [hashmap[k] for k in hashmap if len(hashmap[k]) > 1]

def filedups():
    result = ''
    for entry in list_filedups():
        e = entry[-1].split('/')[-1]
        result += '<img src="/image/%s" alt="%s" /><br />%s ' %(e, e, e)
    return result

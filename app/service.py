# -.- coding: UTF-8 -.-

from os import path, listdir, rename
from json import dumps, loads
from time import time, strftime
from random import sample, choice
from urllib2 import urlopen
from flask import flash
from config import c_file, folder_list, i_default, contentdir, batch_size, p_public, p_reject, statusjsonurl
from log import logger

def write_json(filename, data):
    with open(filename, 'w') as f:
        try:
            f.write(dumps(data, indent=2))
        except Exception:
            pass

def read_json(filename):
    if path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return loads(f.read())
            except Exception:
                pass

def uhr():
    return strftime('%H:%M')

def datum():
    return strftime('%d. %b %Y')

def timestamp_now():
    return int(time())

def list_images(folder):
    if path.exists(folder):
        for filename in listdir(folder):
            if any(filename.endswith(x) for x in ('jpeg', 'jpg', 'png', 'gif')):
                if(path.getsize(path.join(folder, filename)) > 0):
                    yield filename

def mk_content_cache():
    cache = {'timestamp': timestamp_now()}
    for folder, name in folder_list:
        listing = list_images(folder)
        cache[name] = [p for p in listing]
    write_json(c_file, cache)

def read_cache():
    cache = read_json(c_file)
    if cache is None:
        mk_content_cache()
        return read_cache()
    return cache

def list_all_images():
    cache = read_cache()
    result = []
    for f, name in folder_list:
        result += cache[name]
    return result

def get_image_stats():
    cache = read_cache()
    result = {
        'public': len(cache['public']),
        'unsorted': len(cache['unsorted']),
        'reject': len(cache['reject']),
    }
    return result

def get_batch_of_images(field='public', bsize=batch_size):
    cache = read_cache()
    n = bsize if len(cache[field]) > bsize else len(cache[field])
    return sample(cache[field], n)

def get_sort_image():
    mk_content_cache()
    cache = read_cache()
    if len(cache['unsorted']) >= 1:
        logger.info('returned one image to sort')
        return choice(cache['unsorted'])
    logger.error('could not return any image to sort')
    return i_default

def find_image_path(image=i_default):
    cache = read_cache()
    for folder, name in folder_list:
        if image in cache[name]:
            return folder
    logger.info('image %s not found - returning contentdir: %s' %(image, contentdir))
    return contentdir

def move_image(request):
    if 'plus' in request:
        target = p_public
        flashmsg = '+'
    elif 'minus' in request:
        target = p_reject
        flashmsg = '-'
    else:
        logger.error('request makes no sense: %s' %(request))
        return
    source = find_image_path(request['image'])
    if source != contentdir:
        try:
            rename(path.join(source, request['image']), path.join(target, request['image']))
            flash('%s %s' %(flashmsg, request['image']))
        except (OSError, Exception) as e:
            logger.error('could not move: %s -> %s' %(path.join(source, request['image']), path.join(target, request['image'])))
        else:
            logger.info('moved: %s -> %s' %(path.join(source, request['image']), path.join(target, request['image'])))

def scrape(url):
    try:
        logger.info('scraping: %s' %(url))
        return urlopen(url).read()
    except Exception as e:
        logger.info('scrape error: %s  %s' %(url, e))
        return 'error'

def json_status():
    try:
        return loads(scrape(statusjsonurl))
    except Exception as e:
        logger.info('could not refresh json: %s' %(e))
    else:
        logger.info('json refreshed')
    return 'error'

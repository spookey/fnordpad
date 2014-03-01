# -.- coding: UTF-8 -.-

from os import path, listdir, rename
from json import loads
from time import time, strftime
from random import sample, choice
from redis import Redis
from requests import get as rget
from flask import flash
from config import REDIS_host, REDIS_port, REDIS_dbnr, image_folders, i_default, contentdir, batch_size, p_public, p_reject, shout_channel, statusjsonurl
from log import logger

redisDB = Redis(host=REDIS_host, port=REDIS_port, db=REDIS_dbnr, decode_responses=True)

def datum():
    return strftime('%d. %b %Y')

def timestamp_now():
    return int(time())

#

def shout_stream():
    pubsub = redisDB.pubsub()
    pubsub.subscribe(shout_channel)
    for event in pubsub.listen():
        logger.info('new pubsub event: %s' %(event))
        if event['type'] == 'message':
            strdata = 'data: %s\r\n\r\n' %(event['data'])
            yield strdata.encode('UTF-8')

def shout_out(message):
    redisDB.publish(shout_channel, message)

#

def mk_image_cache():
    for name in image_folders:
        redisDB.delete(name)
        for img in list_images(image_folders[name]):
            redisDB.rpush(name, img)
    logger.info('Image cache generated')

def read_image_cache():
    result = dict()
    for name in image_folders:
        result[name] = redisDB.lrange(name, 0, -1)
    return result

def list_images(folder):
    if path.exists(folder):
        for filename in listdir(folder):
            if any(filename.endswith(x) for x in ('jpeg', 'jpg', 'png', 'gif')):
                if path.getsize(path.join(folder, filename)) > 0:
                    yield filename

def list_all_images():
    cache = read_image_cache()
    result = list()
    for elems in cache:
        result += cache[elems]
    return result

def get_image_stats():
    result = dict()
    for name in image_folders:
        result[name] = redisDB.llen(name)
    return result

def get_batch_of_images(field='public', bsize=batch_size):
    cache = read_image_cache()
    n = bsize if len(cache[field]) > bsize else len(cache[field])
    return sample(cache[field], n)

def get_sort_image():
    cache = read_image_cache()
    imgleft = len(cache['unsorted'])
    if imgleft >= 1:
        logger.info('returned one image to sort')
        return choice(cache['unsorted']), imgleft
    logger.warn('no images left for sorting')
    return i_default, imgleft

def find_image_path(image, fullpath=True):
    cache = read_image_cache()
    for line in cache:
        if image in cache[line]:
            return image_folders[line] if fullpath else line
    logger.info('image %s not found - returning contentdir: %s' %(image, contentdir))
    return contentdir if fullpath else None

def move_image(requestform):
    if 'plus' in requestform:
        targettag = 'public'
        flashstate = '+'
    elif 'minus' in requestform:
        targettag = 'reject'
        flashstate = '-'
    else:
        logger.error('request makes no sense: %s' %(requestform))
        return
    source = find_image_path(requestform['image'])
    if source != contentdir:
        sourcetag = find_image_path(requestform['image'], fullpath=False)
        target = image_folders[targettag]
        try:
            rename(path.join(source, requestform['image']), path.join(target, requestform['image']))
            redisDB.rpush(targettag, requestform['image'])
            redisDB.lrem(sourcetag, requestform['image'])
            flash('%s %s' %(flashstate, requestform['image']))
        except (OSError, Exception) as e:
            logger.error('could not move: %s -> %s' %(path.join(source, requestform['image']), path.join(target, requestform['image'])))
        else:
            logger.info('moved: %s -> %s' %(path.join(source, requestform['image']), path.join(target, requestform['image'])))

#

def scrape(url):
    try:
        logger.info('scraping: %s' %(url))
        return rget(url).text
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

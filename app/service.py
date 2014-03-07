# -.- coding: UTF-8 -.-

from os import path, listdir, rename
from json import loads
from time import time
from random import choice
from redis import Redis
from requests import get as rget
from flask import flash
from config import REDIS_host, REDIS_port, REDIS_dbnr, image_folders, i_default, contentdir
from log import logger

redisDB = Redis(host=REDIS_host, port=REDIS_port, db=REDIS_dbnr, decode_responses=True)

def timestamp_now():
    return int(time())

#

def shout_to_browser(channel):
    pubsub = redisDB.pubsub()
    pubsub.subscribe(channel)
    for event in pubsub.listen():
        logger.info('new pubsub event: %s' %(event))
        if event['type'] == 'message':
            strdata = 'data: %s\r\n\r\n' %(event['data'].replace('\n', '<br />'))
            yield strdata.encode('UTF-8')

def shout_to_redis(channel, message):
    redisDB.publish(channel, message)

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

def get_image(field='public'):
    cache = read_image_cache()
    return choice(cache[field]) if redisDB.llen(field) > 0 else i_default

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
            logger.error('could not move: %s -> %s (%s)' %(path.join(source, requestform['image']), path.join(target, requestform['image']), e))
        else:
            logger.info('moved: %s -> %s' %(path.join(source, requestform['image']), path.join(target, requestform['image'])))

#

def scrape_status(url):
    feed = None
    try:
        logger.info('scraping: %s' %(url))
        feed = rget(url).text
    except Exception as e:
        logger.info('scrape error: %s  %s' %(url, e))
    else:
        redisDB.set('statusjson', feed)
        logger.info('json refreshed')


def json_status():
    return loads(redisDB.get('statusjson'))

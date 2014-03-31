# -.- coding: UTF-8 -.-

from os import path, listdir, rename
from json import loads
from time import time
from random import choice
from requests import get as rget
from flask import flash
from config import image_folders, i_default, contentdir, image_channel
from app import app
from log import logger

def timestamp_now():
    return int(time())

#

def shout_to_browser(channel):
    pubsub = app.redisDB.pubsub()
    pubsub.subscribe(channel)
    for event in pubsub.listen():
        logger.info('new pubsub event: %s' %(event))
        if event['type'] == 'message':
            strdata = 'data: %s\r\n\r\n' %(event['data'].replace('\n', '<br />'))
            yield strdata.encode('UTF-8')

def shout_to_redis(channel, message):
    app.redisDB.publish(channel, message)
    return message

#

def next_image():
    return shout_to_redis(image_channel, get_image())

def mk_image_cache():
    for name in image_folders:
        app.redisDB.delete(name)
        for img in list_images(image_folders[name]):
            app.redisDB.rpush(name, img)
    logger.info('Image cache generated')

def read_image_cache():
    result = dict()
    for name in image_folders:
        result[name] = app.redisDB.lrange(name, 0, -1)
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
        result[name] = app.redisDB.llen(name)
    return result

def get_image(field='public'):
    cache = read_image_cache()
    return choice(cache[field]) if app.redisDB.llen(field) > 0 else i_default

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
            app.redisDB.rpush(targettag, requestform['image'])
            app.redisDB.lrem(sourcetag, requestform['image'])
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
        app.redisDB.set('statusjson', feed)
        logger.info('json refreshed')


def json_status():
    status = app.redisDB.get('statusjson')
    if status:
        return loads(status)


from  threading import Timer

class RepeatingTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.interval = interval
    def start(self):
        self.callback()
    def stop(self):
        self.interval = False
    def callback(self):
        if self.interval:
            self.function(*self.args, **self.kwargs)
            Timer(self.interval, self.callback, ).start()

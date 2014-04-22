'''config file'''

from os import path

## General
BASEDIR = path.abspath(path.dirname(__file__))
LOGDIR = path.join(BASEDIR, 'logs')
LOGFILE = path.join(LOGDIR, 'fnordpad.log')

SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'
#>>> import os
#>>> os.urandom(24)

CONTENTDIR = path.join(BASEDIR, 'app/static/content')

NULLIMG = 'fnord.jpeg'              # fallback/default image

CONTENTSUB = {
    'unsorted': path.join(CONTENTDIR, 'unsorted'),
    'public': path.join(CONTENTDIR, 'public'),
    'reject': path.join(CONTENTDIR, 'reject'),
}
IMAGEEXTENSIONS = ['jpeg', 'jpg', 'png', 'gif']

## Redis
REDIS_OPT = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
    'decode_responses': True,
    'image_prefix': 'images',       # db prefix for images
    'image_pubsub': 'image',        # pubsub channel images
    'image_timeout': 15,            # seconds
    'sort_slices': 9,               # sort pagination
    'shout_pubsub': 'shout',        # pubsub channel shout
    'status_prefix': 'status',      # db prefix for status json data
    'status_expire': 60*15,         # Seconds
    'status_url': 'http://status.cccmz.de/api/latest/get/all/last/',
}

TAGLINES = ['It\'s Peanut Butter Jelly Time', 'Your ad here!', 'This page intentionally left blank', 'Lorem ipsum dolor sit amet']

SOUPPAGES = 50
SOUPUSERS = [
    'fnordpad',
    'gnd',
    'cccmz',
    'sixtus',
    'lambda',
    'againstreality',
    'kv0',
    'maesto',
    'i8br',
    'amenthes',
    'murmeltier',
    'fotochaoten',
    'kochchaoten',
    'hipsterhackers',
    'rocco-the-spoon',
    'saper',
    'tokei',
    'lsanoj',
    'markusbec',
    'sapling'
    ]

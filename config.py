# -.- coding: UTF-8 -.-

'''fnordpad config file'''

from os import path

## General
basedir = path.abspath(path.dirname(__file__))
contentdir = path.join(basedir, 'content')

logdir = path.join(basedir, 'logs')
logfile = path.join(logdir, 'logfile.log')


## Flask
SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'
#>>> import os
#>>> os.urandom(24)
USE_X_SENDFILE = True


## Redis
REDIS_host = 'localhost'
REDIS_port = 6379
REDIS_dbnr = 1

image_channel = 'image'
shout_channel = 'shout'

## Images
i_default = 'fnord.jpeg' # fallback/default image

image_folders = {
    'unsorted': path.join(contentdir, 'unsorted'),
    'public': path.join(contentdir, 'public'),
    'reject': path.join(contentdir, 'reject'),
}

batch_size = 23

statusjsonurl = 'http://status.cccmz.de/api/0.2/get/all/last/'


## Suppenkasper
soupusers = ['fnordpad', 'gnd', 'cccmz', 'sixtus', 'lambda', 'againstreality', 'kv0', 'maesto', 'i8br', 'amenthes', 'murmeltier', 'fotochaoten', 'kochchaoten', 'hipsterhackers', 'rocco-the-spoon', 'saper', 'tokei', 'lsanoj', 'markusbec', 'sapling']
crawl_pages = 50


## etc
taglines = ['It\'s Peanut Butter Jelly Time', 'Your ad here!', 'This page intentionally left blank', 'Lorem ipsum dolor sit amet']

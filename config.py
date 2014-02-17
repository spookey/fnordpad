# -.- coding: UTF-8 -.-

from os import path

basedir = path.abspath(path.dirname(__file__))

staticdir = path.join(basedir, 'app/static/')
cachedir = path.join(basedir, 'cache')
c_file = path.join(cachedir, 'content.json')

contentdir = path.join(basedir, 'content')
i_default = 'fnord.jpeg'
p_unsorted = path.join(contentdir, 'unsorted')
p_public = path.join(contentdir, 'public')
p_reject = path.join(contentdir, 'reject')
folder_list = list(zip([p_unsorted, p_public, p_reject], ['unsorted', 'public', 'reject']))

batch_size = 23

statusjsonurl = 'http://status.cccmz.de/api/0.2/get/all/last/'

logdir = path.join(basedir, 'logs')
logfile = path.join(logdir, 'logfile.log')

#>>> import os
#>>> os.urandom(24)
SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'

USE_X_SENDFILE = True

# Crawler
soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'lambda', 'againstreality', 'kv0', 'maesto', 'i8br', 'amenthes', 'murmeltier', 'fotochaoten', 'kochchaoten', 'hipsterhackers', 'rocco-the-spoon', 'saper', 'tokei', 'lsanoj', 'markusbec', 'sapling']
crawl_pages = 50

taglines = ['It\'s Peanut Butter Jelly Time', 'Your ad here', 'This page intentionally left blank', 'Lorem ipsum dolor sit amet']

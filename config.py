# -.- coding: UTF-8 -.-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

staticdir = os.path.join(basedir, 'app/static/')

p_folder = os.path.join(basedir, 'content')
p_unsorted = os.path.join(p_folder, 'unsorted')
p_public = os.path.join(p_folder, 'public')
p_reject = os.path.join(p_folder, 'reject')
i_default = os.path.join(p_folder, 'fnord.jpeg')

logfile = os.path.join(basedir, 'logfile.log')

#>>> import os
#>>> os.urandom(24)
SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'

USE_X_SENDFILE = True

# Crawler
soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'lambda', 'againstreality', 'kv0', 'maesto', 'i8br', 'amenthes', 'murmeltier', 'fotochaoten', 'kochchaoten', 'hipsterhackers', 'rocco-the-spoon', 'saper', 'tokei', 'lsanoj', 'markusbec', 'sapling']
crawl_pages = 50
crawl_verbose = False

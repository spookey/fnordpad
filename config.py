# -.- coding: UTF-8 -.-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

staticdir = os.path.join(basedir, 'app/static/')

p_folder = os.path.join(basedir, 'content')
p_unsorted = os.path.join(p_folder, 'unsorted')
p_public = os.path.join(p_folder, 'public')
p_reject = os.path.join(p_folder, 'reject')
i_default = os.path.join(p_folder, 'fnord.jpeg')

SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'
USE_X_SENDFILE = True

# Crawler
soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'fotochaoten', 'kochchaoten', 'hipsterhackers']

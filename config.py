# -.- coding: UTF-8 -.-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

staticdir = os.path.join(basedir, 'app/static/')

subf = 'app/static/bilder/'
p_unsorted = os.path.join(basedir, subf, 'unsorted')
p_public = os.path.join(basedir, subf, 'public')
p_reject = os.path.join(basedir, subf, 'reject')

SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'

soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'fotochaoten', 'kochchaoten', 'hipsterhackers']

# -.- coding: UTF-8 -.-

import os, logging
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))

staticdir = os.path.join(basedir, 'app/static/')

p_folder = os.path.join(basedir, 'content')
p_unsorted = os.path.join(p_folder, 'unsorted')
p_public = os.path.join(p_folder, 'public')
p_reject = os.path.join(p_folder, 'reject')
i_default = os.path.join(p_folder, 'fnord.jpeg')

logfile = os.path.join(basedir, 'logfile.log')

filehandler = RotatingFileHandler(logfile, 'a', 1 * 1024 * 1024, 23)
filehandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'))

logger = logging.getLogger('fnordpad')
logger.setLevel(logging.INFO)
logger.addHandler(filehandler)

SECRET_KEY = 'Geheimen Schlüssel hier einfügen, sonst setzts was!!1!'

USE_X_SENDFILE = True

# Crawler
soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'fotochaoten', 'kochchaoten', 'hipsterhackers']
crawl_verbose = False

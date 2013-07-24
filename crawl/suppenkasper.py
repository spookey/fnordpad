# -.- coding: UTF-8 -.-

import sys, os, subprocess
from parser import SoupParser

sys.path.insert(0, '/var/www/fnordpad/')

from config import p_unsorted, p_public, p_reject, soupusers, crawlog, crawl_verbose
from app.service import list_all_images

from logging import getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler

filehandler = RotatingFileHandler(crawlog, 'a', 1 * 1024 * 1024, 23)
filehandler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'))

logger = getLogger('suppenkasper')
logger.setLevel(INFO)
logger.addHandler(filehandler)


def load():
    loadlist = []

    for user in soupusers:
        sp = SoupParser(user, 15, crawl_verbose)
        loadlist.extend(sp.parse())
        del sp
        logger.info('finished parsing for %s' %(user))

    for element in loadlist:
        proc = ['wget', '-c', '-P', p_unsorted, element]

        if crawl_verbose:
            proc.insert(1, '-v')
        else:
            proc.insert(1, '-nv')

        if not element.split('/')[-1] in list_all_images():
            subprocess.call(proc)
            logger.info('downloaded %s' %(element))
        else:
            if crawl_verbose:
                print 'Omitted %s' %(element.split('/')[-1])


if __name__ == "__main__":
    crawl_verbose = True
    load()

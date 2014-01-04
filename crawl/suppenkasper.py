# -.- coding: UTF-8 -.-

import sys, subprocess
from parser import SoupParser
from os import path
sys.path.insert(0, path.join(path.abspath(path.dirname(__file__)), '../'))

from config import p_unsorted, soupusers, crawl_pages
from app.service import list_all_images
from log import logger

def load():
    logger.info('suppenkasper started')
    logger.info('-' * 20)
    for user in soupusers:
        logger.info('parsing: %s' %(user))
        sp = SoupParser(user, crawl_pages)
        for element in sp.parse():
            proc = ['wget', '-nv', '-c', '-P', p_unsorted, element]

            if not element.split('/')[-1] in list_all_images():
                subprocess.call(proc)
                logger.info('downloaded %s' %(element))
            else:
                logger.info('omitted %s' %(element.split('/')[-1]))
        del sp
        logger.info('finished parsing for %s' %(user))

if __name__ == "__main__":
    crawl_verbose = True
    load()

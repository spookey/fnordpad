# -.- coding: UTF-8 -.-

import sys, os, subprocess
from parser import SoupParser

sys.path.insert(0, '/srv/www/fnordpad/')

from config import p_unsorted, p_public, p_reject, soupusers, logger, crawl_verbose
from app.service import list_all_images

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
            logger.info('omitted %s' %(element))


if __name__ == "__main__":
    crawl_verbose = True
    load()

# -.- coding: UTF-8 -.-

import sys, os, subprocess
from parser import SoupParser

sys.path.insert(0, '/srv/www/fnordpad/')

from config import p_unsorted, p_public, p_reject, soupusers, logger, crawl_verbose, crawl_pages
from app.service import list_all_images

def load():
    for user in soupusers:

        sp = SoupParser(user, crawl_pages, crawl_verbose)
        for element in sp.parse():
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

        del sp
        logger.info('finished parsing for %s' %(user))



if __name__ == "__main__":
    crawl_verbose = True
    load()

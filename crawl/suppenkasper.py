# -.- coding: UTF-8 -.-

import sys, os, subprocess
from parser import SoupParser

sys.path.insert(0, '/var/www/fnordpad/')

from config import p_unsorted, p_public, p_reject, soupusers, crawl_verbose
from app.service import list_all_images

def load():
    loadlist = []

    for user in soupusers:
        sp = SoupParser(user, 15, crawl_verbose)
        loadlist.extend(sp.parse())
        del sp

    for element in loadlist:
        proc = ['wget', '-c', '-P', p_unsorted, element]

        if crawl_verbose:
            proc.insert(1, '-v')
        else:
            proc.insert(1, '-nv')

        if not element.split('/')[-1] in list_all_images():
            subprocess.call(proc)
        else:
            if crawl_verbose:
                print 'Omitted %s' %(element.split('/')[-1])


if __name__ == "__main__":
    crawl_verbose = True
    load()

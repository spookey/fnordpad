# -.- coding: UTF-8 -.-

import os, subprocess
from parser import SoupParser

from config import p_unsorted, p_public, p_reject, soupusers
from app.service import list_all_images

verbose = False

def load():
    loadlist = []

    for user in soupusers:
        sp = SoupParser(user, 15, verbose)
        loadlist.extend(sp.parse())
        del sp

    for element in loadlist:
        proc = ['wget', '-c', '-P', p_unsorted, element]

        if verbose:
            proc.insert(1, '-v')
        else:
            proc.insert(1, '-nv')

        if not element.split('/')[-1] in list_all_images():
            subprocess.call(proc)
        else:
            if verbose:
                print 'Omitted %s' %(element.split('/')[-1])


if __name__ == "__main__":
    verbose = True
    load()

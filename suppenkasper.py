# -.- coding: UTF-8 -.-

from parser import Soupparser
import os, subprocess

from config import p_unsorted, p_public, p_reject, soupusers
from app.side import imagelist

verbose = False

print imagelist(p_public)

loadlist = []

for user in soupusers:
    sp = Soupparser(user, 15, verbose)
    loadlist.extend(sp.parse())
    del sp

for element in loadlist:
    proc = ['wget', '-c', '-P', p_unsorted, element]

    if verbose:
        proc.insert(1, '-v')
    else:
        proc.insert(1, '-nv')

    if not element.split('/')[-1] in imagelist(p_unsorted) +  imagelist(p_public) + imagelist(p_reject):
        subprocess.call(proc)


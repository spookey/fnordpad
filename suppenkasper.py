#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Parser import soupparser
import os, subprocess

# Zielordner der Bilder
targetfolder = os.path.expanduser('~/bilder')
verbose = False

soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'fotochaoten', 'kochchaoten', 'hipsterhackers']

loadlist = []

for user in soupusers:
    sp = soupparser(user, 15, verbose)
    loadlist.extend(sp.parse())
    del sp

if not os.path.exists(targetfolder):
    os.mkdir(targetfolder)

for element in loadlist:
    proc = ['wget', '-c', '-P', targetfolder, element]

    if verbose:
        proc.insert(1, '-v')
    else:
        proc.insert(1, '-nv')

    subprocess.call(proc)


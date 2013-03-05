#!/usr/bin/env python
# -*- coding: utf-8 -*-

from soupparser import Soupparser
import os, subprocess

# Zielordner der Bilder
targetfolder = os.path.expanduser('~/Desktop/sucking')
verbose = False

soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'fotochaoten', 'kochchaoten', 'hipsterhackers']

loadlist = []

for user in soupusers:
	sp = Soupparser(user, 5, verbose)
	loadlist.extend(sp.parse())
	del sp

if not os.path.exists(targetfolder):
	os.mkdir(targetfolder)
for element in loadlist:
	subprocess.call(['wget', '-nv', '-c', '-P', targetfolder, element])

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from soupparser import soupparser
import os, subprocess

# Zielordner der Bilder
targetfolder = os.path.expanduser('~/Desktop/sucking')
if not os.path.exists(targetfolder):
	os.mkdir(targetfolder)

soupusers=['fnordpad', 'gnd', 'cccmz', 'sixtus', 'fotochaoten', 'kochchaoten', 'hipsterhackers']

verbose = False

loadlist = []

for user in soupusers:
	sp = soupparser(user, 2, verbose)
	loadlist.extend(sp.parse())
	del sp

for element in loadlist:
	subprocess.call(['wget', '-nv', '-c', '-P', targetfolder, element])
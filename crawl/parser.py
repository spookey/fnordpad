# -*- coding: utf-8 -*-

import urllib, re, argparse, sys
from os import path
sys.path.insert(0, path.join(path.abspath(path.dirname(__file__)), '../'))
from log import logger

class SoupParser(object):

    # Vielen Dank an Frank für diese Awesome Regex!
    __rx = r'(url|src)="(http://asset-.\.soup\.io/asset/\d{4}/.{4}_.{4})(_.*)?\.(jpeg|jpg|gif|png)'
    __sx = r'SOUP.Endless.next_url.*/(since/\d*)'

    def __init__(self, soupuser, pages):
        self.__soupuser = soupuser
        self.__pages = pages

    def __crawl(self, url):
        images = []
        since = ''
        code = urllib.urlopen(url).read()
        for line in code.split('\n'):
            imagesearch = re.search(self.__rx, line)
            if imagesearch and not re.search('square', imagesearch.group(0)):
                image = '%s.%s' % (imagesearch.group(2), imagesearch.group(4))
                images.append(image)
            if re.search(self.__sx, line):
                since = re.search(self.__sx, line).group(1)
        return images, since

    def _soupfeed(self):
        url='http://%s.soup.io/rss/' %(self.__soupuser)
        logger.info('Finished Feed for %s' %(self.__soupuser))
        return self.__crawl(url)[0]

    def _soupweb(self, loops):
        images = []
        since = ''
        for loop in range(0, loops):
            url='http://%s.soup.io/%s' %(self.__soupuser, since)
            result = self.__crawl(url)
            images.extend(result[0])
            since = result[1]
            logger.info('Finished Page %d of %d for %s' %(loop + 1, loops, self.__soupuser))
        return images

    def parse(self):
        # Entfernt doppelte Einträge
        images = set(self._soupfeed())
        images.update(self._soupweb(self.__pages))
        logger.info('Finished Feed and all Pages for %s' %(self.__soupuser))
        return images

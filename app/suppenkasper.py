# -.- coding: utf-8 -.-

from config import p_unsorted, soupusers, crawl_pages
from .service import list_all_images
from log import logger
import re
from os import path
from multiprocessing import Pool
from requests import get as rget

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
        code = rget(url).text
        for line in code.split('\n'):
            imagesearch = re.search(self.__rx, line)
            if imagesearch and not re.search('square', imagesearch.group(0)):
                image = '%s.%s' % (imagesearch.group(2), imagesearch.group(4))
                images.append(image)
            if re.search(self.__sx, line):
                since = re.search(self.__sx, line).group(1)
        return images, since

    def _soupweb(self, loops):
        images = []
        since = ''
        for loop in range(0, loops):
            url='http://%s.soup.io/%s' %(self.__soupuser, since)
            result = self.__crawl(url)
            images.extend(result[0])
            since = result[1]
            logger.info('Finished %d/%d for %s' %(loop + 1, loops, self.__soupuser))
        return images

    def parse(self):
        # Entfernt doppelte Einträge
        images = set(self._soupweb(self.__pages))
        logger.info('Finished for %s' %(self.__soupuser))
        return images


def dload(urllist):
    for url in urllist:
        filename = url.split('/')[-1]
        r = rget(url, stream=True)
        if r.status_code == 200:
            with open(path.join(p_unsorted, filename), 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            logger.info('.done: %s' %(filename))

def kasper(view=True):
    startmsg = 'suppenkasper started'
    logger.info(startmsg)
    logger.info('-' * len(startmsg))

    loadurls = list()
    allimages = list_all_images()

    for user in soupusers:
        logger.info('parsing %s' %(user))

        loadurls += [url for url in SoupParser(user, crawl_pages).parse() if url.split('/')[-1] not in allimages]

    endmsg = 'crawl finished'
    logger.info(endmsg)
    logger.info('-' * len(endmsg))

    response = '%s Elements:<br />' %(len(loadurls))
    for url in loadurls:
        response += '%s <br />' %(url.split('/')[-1])

    if view == 'load':
        dload(loadurls)
        return response
    else:
        return response

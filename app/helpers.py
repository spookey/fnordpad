'''helps'''

from os import path
from requests import get as rget, session as rsession
from config import CONTENTSUB
from app.log import LOGGER

class Net(object):
    '''does network stuff'''

    __cookie = None

    def __init__(self):
        super().__init__()
        LOGGER.info('new net instance')

    def url_scrape(self, url, split=False):
        try:
            LOGGER.info('scraping %s' %(url))
            return rget(url).text.split('\n') if split else rget(url).text
        except Exception as ex:
            LOGGER.error('scrape error %s %s' %(url, ex))

    def download_image(self, url):
        try:
            LOGGER.info('downloading %s' %(url))
            filename = url.split('/')[-1]
            r = rget(url, stream=True)
            if r.status_code == 200:
                with open(path.join(CONTENTSUB['unsorted'], filename), 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                LOGGER.info('done: %s' %(filename))
        except Exception as ex:
            LOGGER.error('download error %s %s' %(url, ex))

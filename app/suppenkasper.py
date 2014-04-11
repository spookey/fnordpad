'''suppenkasper'''

from re import search as research
from config import SOUPUSERS, SOUPPAGES
from app.helpers import Net
from app.proc import tpool
from app.log import LOGGER
from app import RDB

class Suppenkasper(object):

    __net = None
    _users = None
    __scrape = None

    # Vielen Dank an Frank für diese Awesome Regex!
    __img_rx = r'(url|src)="(http://asset-.\.soup\.io/asset/\d{4}/.{4}_.{4})(_.*)?\.(jpeg|jpg|gif|png)'
    __nxt_rx = r'SOUP.Endless.next_url.*/(since/\d*)'

    def __init__(self):
        super().__init__()
        if not self.__net:
            self.__net = Net()
        if not self._users:
            self._users = SOUPUSERS
        LOGGER.info('new suppenkasper instance')

    def __nextsince(self):
        for line in self.__scrape:
            if research(self.__nxt_rx, line):
                return research(self.__nxt_rx, line).group(1)
        return ''

    def __pageimages(self):
        for line in self.__scrape:
            imagesearch = research(self.__img_rx, line)
            if imagesearch and not research('square', imagesearch.group(0)):
                yield '%s.%s' % (imagesearch.group(2), imagesearch.group(4))
        return ''

    def _usercrawl(self, user, loops=SOUPPAGES):
        since = ''
        for loop in range(loops):
            url = 'http://{user}.soup.io/{since}'.format(user=user, since=since)
            self.__scrape = self.__net.url_scrape(url, split=True)
            since = self.__nextsince()
            LOGGER.info('finished page %d/%d for %s' %(loop+1, loops, user))
            for image in self.__pageimages():
                yield image

    def kasper(self):
        load = list()
        for user in self._users:
            LOGGER.info('kasper %s' %(user))
            for image in self._usercrawl(user):
                if image.split('/')[-1] not in RDB.get_all_images():
                    load.append(image)
                    yield user, image
        tpool(self.__net.download_image, load)

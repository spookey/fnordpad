'''redabas as a service'''

from redis import StrictRedis
from redis.exceptions import ConnectionError as RedisConnectionError
from json import loads
from random import choice
from app.log import LOGGER
from app.files import Files
from app.helpers import Net
from app.proc import Cycle

class Redabas(object):
    '''docstring for redabas'''
    __rdb = None
    __redis_opt = None
    __files = None
    __net = None
    __proc = None

    def __init__(self, redis_opt):
        super().__init__()
        if not self.__rdb:
            self.__rdb = StrictRedis(
                host=redis_opt['host'],
                port=redis_opt['port'],
                db=redis_opt['db'],
                decode_responses=redis_opt['decode_responses']
                )
            self.__redis_opt = redis_opt
            LOGGER.info('created new redis connection')
        if not self.__files:
            self.__files = Files()
        if not self.__net:
            self.__net = Net()
        if not self.__proc:
            self.__proc = Cycle(redis_opt['image_timeout'], self.next_image, ).start()
            pass

    def redis_ping(self):
        if self.__rdb:
            try:
                LOGGER.info('redis ping')
                return self.__rdb.ping()
            except RedisConnectionError as ex:
                LOGGER.error('could not ping redis: %s' %(ex))

        return False

    def get_ropt(self, field):
        if field in self.__redis_opt.keys():
            return self.__redis_opt[field]

    def flush_all(self):
        rdbfields = list()
        for folder in self.__files.get_contentsub(full=False):
            rdbfields.append('%s:%s' %(self.__redis_opt['image_prefix'], folder))
        rdbfields.append('%s:feed' %(self.__redis_opt['status_prefix']))

        for entry in rdbfields:
            self.__rdb.delete(entry)
            LOGGER.info('flushed data for %s' %(entry))

    #

    def get_images(self, folder='public'):
        '''gets images from redis'''
        result = list()
        rdbfield = '%s:%s' %(self.__redis_opt['image_prefix'], folder)

        def __readin():
            '''reloads db'''
            self.__rdb.delete(rdbfield)
            for image in self.__files.find_images(folder=folder):
                self.__rdb.rpush(rdbfield, image)
                result.append(image)
            LOGGER.info('rebuilt redis image cache for %s' %(rdbfield))
            return result

        if folder in self.__files.get_contentsub():
            result = sorted(self.__rdb.lrange(rdbfield, 0, -1))
            return result if result else __readin()

    def __dblocate_image(self, name):
        for folder in self.__files.get_contentsub(full=False):
            if name in self.get_images(folder):
                return folder

    def locate_image(self, name):
        '''locates images'''
        folder = self.__dblocate_image(name)
        if folder:
            LOGGER.info('found requested image %s in folder %s' %(name, folder))
            image = self.__files.jinja_static_file(name, folder=folder)
            if image:
                return image
        LOGGER.info('requested image %s not found' %(name))
        return self.__files.jinja_nullimg()

    def get_imagestats(self):
        '''counts images'''
        result = dict()
        for folder in self.__files.get_contentsub(full=False):
            result[folder] = len(self.get_images(folder=folder))
        return result

    def get_all_images(self):
        '''suppenkasper needs a list of all images'''
        result = list()
        for folder in self.__files.get_contentsub(full=False):
            result += (self.get_images(folder=folder))
        return result

    def get_dict_images(self, folder):
        result = dict()
        if folder in self.__files.get_contentsub(full=False):
            for image in sorted(self.get_images(folder=folder)):
                result[image] = self.locate_image(image)
            return result

    def get_sort_images(self, folder='unsorted', page=0):
        '''batch of images to sort'''
        result = dict()
        if folder in self.__files.get_contentsub(full=False):
            for image in sorted(self.get_images(folder=folder))[page*self.__redis_opt['sort_slices']:page*self.__redis_opt['sort_slices']+self.__redis_opt['sort_slices']]:
                result[image] = self.locate_image(image)
            return result

    def random_image(self, folder='public'):
        '''just one of those images'''
        if folder in self.__files.get_contentsub(full=False):
            images = self.get_images(folder)
            if images:
                result = self.locate_image(choice(images))
                return result if result else self.__files.jinja_nullimg()

    def move_image(self, name, target):
        '''moves images'''
        folder = self.__dblocate_image(name)
        if folder and target in self.__files.get_contentsub(full=False):
            sourcefile = self.__files.jinja_static_file(name, folder=folder, full=True)
            targetfile = self.__files.path_join(target, name)
            if sourcefile and targetfile:
                rdbsourcefield = '%s:%s' %(self.__redis_opt['image_prefix'], folder)
                rdbtargetfield = '%s:%s' %(self.__redis_opt['image_prefix'], target)
                self.__rdb.rpush(rdbtargetfield, name)
                self.__rdb.lrem(rdbsourcefield, 0, name)
                self.__files.file_rename(sourcefile, targetfile)
                print('<- %s\n-> %s\n[ %s %s ]\n\n' %(sourcefile, targetfile, rdbsourcefield, rdbtargetfield))

    #

    def get_status(self):
        '''gets status from redis'''
        result = dict()
        rdbfield = '%s:feed' %(self.__redis_opt['status_prefix'])

        def __readin():
            '''reloads db'''
            self.__rdb.delete(rdbfield)
            result = self.__net.url_scrape(self.__redis_opt['status_url'])
            if result:
                self.__rdb.set(rdbfield, result)
                self.__rdb.expire(rdbfield, self.__redis_opt['status_expire'])
                LOGGER.info('rebuilt redis status cache for %s, again after %i seconds' %(rdbfield, self.__redis_opt['status_expire']))
                return loads(result)

        result = self.__rdb.get(rdbfield)
        return loads(result) if result else __readin()

    #

    def browser_shout(self, channel):
        pubsub = self.__rdb.pubsub()
        pubsub.subscribe(channel)
        for event in pubsub.listen():
            LOGGER.info('shouting to browser channel:%s message:%s' %(channel, event['data']))
            if event['type'] == 'message':
                strdata = 'data: %s\r\n\r\n' %(event['data'].replace('\n', '<br />'))
                yield strdata.encode('UTF-8')

    def redis_shout(self, channel, message):
        LOGGER.info('shouting to redis channel:%s message:%s' %(channel, message))
        self.__rdb.publish(channel, message)
        return message

    #

    def next_image(self):
        '''shout next random image from public to redis'''
        image = self.random_image(folder='public')
        if image:
            LOGGER.info('shouting next image: %s' %(image))
            self.redis_shout(self.__redis_opt['image_pubsub'], image)
            print('shouting next image: %s' %(image))

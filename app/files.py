'''where is my content'''

from os import rename, path, listdir, remove
from hashlib import sha1
from config import CONTENTDIR, NULLIMG, CONTENTSUB, IMAGEEXTENSIONS
from app.log import LOGGER

class Files(object):
    '''deals with content'''
    __contentdir = CONTENTDIR
    __nullimg = NULLIMG
    __contentsub = CONTENTSUB

    def __init__(self):
        super().__init__()

    def get_contentdir(self):
        '''location of CONTENTDIR'''
        return self.__contentdir
    def get_nullimg(self, full=True):
        '''fallback image'''
        return path.join(self.__contentdir, self.__nullimg) if full else self.__nullimg
    def get_contentsub(self, full=False):
        return self.__contentsub if full else self.__contentsub.keys()

    def find_images(self, folder='public'):
        '''find ALL the pictures'''
        if folder in self.get_contentsub(full=False):
            for filename in listdir(self.get_contentsub(full=True)[folder]):
                if any(filename.endswith(x) for x in IMAGEEXTENSIONS):
                    if path.getsize(path.join(self.get_contentsub(full=True)[folder], filename)) > 0:
                        yield filename

    def path_join(self, folder, name):
        if folder in self.get_contentsub(full=False):
            return path.join(self.get_contentsub(full=True)[folder], name)

    def file_rename(self, source, target):
        if path.exists(source):
            LOGGER.info('moved %s to %s' %(source, target))
            rename(source, target)

    def jinja_nullimg(self, full=False):
        return self.get_nullimg(full=True) if full else '/'.join(self.get_nullimg(full=True).split('/')[-2:])

    def jinja_static_file(self, name, folder='public', full=False):
        '''returns jinja filepath for static filenames'''
        if folder in self.get_contentsub(full=False):
            fullfile = self.path_join(folder, name)
            if path.exists(fullfile):
                LOGGER.info('file exists')
                return fullfile if full else '/'.join(fullfile.split('/')[-3:])

class Duplicates(object):
    '''checks for duplicate images'''

    __files = None
    __hashalg = sha1

    def __init__(self):
        super().__init__()
        if not self.__files:
            self.__files = Files()
        LOGGER.info('new duplicates instance')

    def __chunk_reader(self, fileobj, chunk_size=1024):
        '''reads opened file in chunks'''
        while True:
            chunk = fileobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def check(self):
        hashmap = dict()
        match = 0
        subfolders = self.__files.get_contentsub(full=True)
        for folder in subfolders:
            for filename in listdir(subfolders[folder]):
                currentfile = self.__files.path_join(folder, filename)
                if any(currentfile.endswith(x) for x in IMAGEEXTENSIONS):
                    hashobj = self.__hashalg()
                    with open(currentfile, 'rb') as fileobj:
                        for chunk in self.__chunk_reader(fileobj):
                            hashobj.update(chunk)
                        fileID = (hashobj.digest(), path.getsize(currentfile))
                        duplicate = hashmap.get(fileID, None)
                        if duplicate:
                            match += 1
                            yield {
                                'image': filename,
                                'imgpath': self.__files.jinja_static_file(
                                    filename, folder=folder, full=False
                                    )
                                }
                        else:
                            hashmap[fileID] = currentfile
        LOGGER.info('found %i duplicate files' %(match))

    def delete(self):
        for dup in self.check():
            fullpath = self.__files.jinja_static_file(
                dup['image'],
                folder=dup['imgpath'].split('/')[-2],
                full=True
                )
            if path.exists(fullpath):
                remove(fullpath)
                print('deleted %s' %(fullpath)) # as explicit warning to the error.log
                LOGGER.info('deleted duplicate %s' %(dup['image']))
                yield {'image': dup['image'], 'imgpath': dup['imgpath']}

        LOGGER.info('no duplicate files deleted')


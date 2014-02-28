# -.- coding: UTF-8 -.-

from sys import argv
from os import path, listdir, remove
from hashlib import sha1


def chunk_reader(fileobject, chunk_size=1024):
    while True:
        chunk = fileobject.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_duplicates(imagepath, hash=sha1, rmdups=False):
    hashmap = {}
    for sfolder in ['public', 'reject', 'unsorted']:
        full_sfolder = path.join(imagepath, sfolder)
        for filename in listdir(full_sfolder):
            currentfile = path.join(full_sfolder, filename)
            hashobject = hash()
            with open(currentfile, 'rb') as fileobject:
                for chunk in chunk_reader(fileobject):
                    hashobject.update(chunk)
                fileID = (hashobject.digest(), path.getsize(currentfile))
                duplicate = hashmap.get(fileID, None)
                if duplicate:
                    duplicatelist = duplicate.split('/')
                    print('\n[%s]\t%s \n[%s]\t%s' %(sfolder, filename, duplicatelist[-2], duplicatelist[-1]))
                    if rmdups:
                        if filename != '.touch':
                            remove(currentfile)
                            print('\t[%s]\t%s deleted ' %(sfolder, filename))
                else:
                    hashmap[fileID] = currentfile

if __name__ == '__main__':
    imagepath = path.join(path.abspath(path.dirname(__file__)), 'content')

    rmflag = False if argv[-1] != 'del' else True
    check_duplicates(imagepath, rmdups=rmflag)

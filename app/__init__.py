'''app'''

from flask import Flask

APP = Flask(__name__)
APP.config.from_object('config')

from app.log import LOGGER
STARTMSG = 'fnordpad started'
LOGGER.info(STARTMSG)
LOGGER.info('=' * len(STARTMSG))

from itertools import cycle
TAGLINES = cycle(APP.config['TAGLINES'])

from app.db import Redabas
from config import REDIS_OPT
RDB = Redabas(REDIS_OPT)

from app.files import Duplicates
DUPLICATES = Duplicates()

from app.suppenkasper import Suppenkasper
SUPPENKASPER = Suppenkasper()

if not RDB.redis_ping():
    DB_ERRMSG = 'redis error'
    LOGGER.error(DB_ERRMSG)
    LOGGER.error('!' * len(DB_ERRMSG))

    @APP.route('/')
    @APP.route('/<brain>/')
    def errorsplash(brain=None):
        '''help - no brain found'''
        LOGGER.info('request was: %s' %(brain))
        return views.redis_error('no brain found: %s' %(DB_ERRMSG))

from app import views

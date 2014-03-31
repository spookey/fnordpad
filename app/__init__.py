# -.- coding: UTF-8 -.-

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

if app.debug is False:
    from log import filehandler
    app.logger.addHandler(filehandler)
    logger = app.logger

logger.info('fnordpad started')
logger.info('=' * 16)

from redis import Redis
from config import REDIS_host, REDIS_port, REDIS_dbnr
app.redisDB = Redis(host=REDIS_host, port=REDIS_port, db=REDIS_dbnr, decode_responses=True)


from app import views

# -.- coding: UTF-8 -.-

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from config import logfile
from log import init_logger
logger = init_logger(logfile, 'fnordpad')

logger.info('fnordpad started')
logger.info('-' * 16)

from app import views

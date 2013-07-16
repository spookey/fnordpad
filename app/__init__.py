# -.- coding: UTF-8 -.-

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from config import logger
logger.info('fnordpad started')
logger.info('-' * 16)

from app import views

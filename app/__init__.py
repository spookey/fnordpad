# -.- coding: UTF-8 -.-

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

if app.debug is not True:
    from log import filehandler
    app.logger.addHandler(filehandler)
    logger = app.logger

logger.info('fnordpad started')
logger.info('-' * 16)

from app import views

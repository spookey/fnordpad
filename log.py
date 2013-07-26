# -.- coding: UTF-8 -.-

from logging import getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler

def init_logger(filename, name='fnordpad'):
    filehandler = RotatingFileHandler(filename, 'a', 1 * 1024 * 1024, 23)
    filehandler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'))

    logger = getLogger(name)
    logger.setLevel(INFO)
    logger.addHandler(filehandler)

    return logger

'''takes notes of everything'''

from config import LOGFILE
from logging import getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler

FILEHANDLER = RotatingFileHandler(LOGFILE, 'a', 1 * 1024 * 1024, 23)
FILEHANDLER.setFormatter(
    Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'
        )
    )

LOGGER = getLogger('fnordpad')
LOGGER.setLevel(INFO)
LOGGER.addHandler(FILEHANDLER)

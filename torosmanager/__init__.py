__version__ = "0.1a2"

from . import preprocessor
from . import config
from . import models
import logging

config.init_logger()
logger = logging.getLogger("init")
logger.info("TOROS Manager Started.")
try:
    config.init_database()
except:
    logger.exception("Error initiating database.")

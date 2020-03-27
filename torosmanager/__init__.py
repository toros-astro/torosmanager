__version__ = "0.1a1"

from . import preprocessor
from . import config
import logging as _logging

config.init_logger()
logger = _logging.getLogger("init")
logger.info("TOROS Manager Started.")
config.init_database()

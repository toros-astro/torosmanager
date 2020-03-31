__version__ = "0.1a1"

from . import preprocessor
from . import config
from . import models

config.init_logger()
import logging as _logging

_logging.getLogger("init").info("TOROS Manager Started.")

config.init_database()

__version__ = "0.1a1"

from . import preprocessor
from . import config

config.init_logger()
config.init_database()

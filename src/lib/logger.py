#!/usr/bin/python

import os
import logging
from lib.system import  *

# variables
NAME = "grape"
LOG_FILE = get_home() + os.sep + NAME + ".log"

# @singleton
class Logger(logging.Logger):
    """Configuration logger class"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton implementation"""
        if not cls.__instance:
            cls.__instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        """Initializes logger configuration"""
        logging.Logger.__init__(self, NAME)

        f = logging.Formatter("%(levelname)s %(asctime)s: %(funcName)s+%(lineno)d: %(message)s")
        h1 = logging.FileHandler(LOG_FILE)
        h1.setFormatter(f)
        h1.setLevel(logging.DEBUG)
        h2 = logging.StreamHandler(sys.stdout)
        h2.setFormatter(f)
        h2.setLevel(logging.DEBUG)
        self.addHandler(h1)
        self.addHandler(h2)
        self.setLevel(logging.DEBUG)

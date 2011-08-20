#!/usr/bin/python

import os
import ConfigParser
from lib.system import  *

# variables
CONFIGFILE = get_full_path(get_local_storage(), ".grape.conf")
SYSTEM_CONFIGFILE = get_full_path(get_system_storage(), "grape.conf")

# @singleton
class Config(object):
    """Configuration parsing class"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton implementation"""
        if not cls.__instance:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, logger = None, defaults = {}):
        """Initializes configuration"""

        if logger:
            self.logger = logger
        self.configfile = CONFIGFILE
        self.master_configfile = SYSTEM_CONFIGFILE
        self.defaults = defaults

    def load(self):
        """Reads configuration"""
        self.config = ConfigParser.ConfigParser(self.defaults)
        try:
            if self.master_configfile:
                self.logger.info("Reading master configfile %s" % self.master_configfile)
                self.config.read(self.master_configfile)
            self.logger.info("Reading configfile %s" % self.configfile)
            self.config.read(self.configfile)
        except:
            self.logger.exception("Reading configfile")

    def save(self):
        """Writes configuration"""
        self.logger.info("Writing configfile %s" % self.configfile)
        try:
            with open(self.configfile, "w") as fd:
                self.config.write(fd)
        except:
            self.logger.exception("Writing configfile")

    def get(self, section, variable, default):
        """Gets a variable from a section of config"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        if not self.config.has_option(section, variable):
            self.config.set(section, variable, default)
        value = self.config.get(section, variable)
        return value

    def set(self, section, variable, default):
        """Sets a variable from a section of config"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, variable, default)



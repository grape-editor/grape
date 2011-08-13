#!/usr/bin/python

import os
import ConfigParser
from lib import system

class Config(object):
    """Configuration parsing class"""
    def __init__(self, logger, configfile, master_configfile=None, defaults={}):
        """Initializes configuration"""
        self.logger = logger
        self.configfile = configfile
        self.master_configfile = master_configfile
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

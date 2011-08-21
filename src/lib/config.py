#!/usr/bin/python

import os
import ConfigParser
from lib.system import  *
from lib.logger import Logger

# variables
CONFIGFILE = get_full_path(get_local_storage(), ".grape.conf")
SYSTEM_CONFIGFILE = get_full_path(get_system_storage(), "grape.conf")

# @singleton
class Config(object):
    """Configuration parsing class"""
    __instance = None
    __defaults_options = False

    def __new__(self, *args, **kwargs):
        """Singleton implementation"""
        if not self.__instance:
            self.__instance = super(Config, self).__new__(self, *args, **kwargs)
        return self.__instance

    def __init__(self):
        """Initializes configuration"""
        self.logger = Logger()
        self.configfile = CONFIGFILE
        self.master_configfile = SYSTEM_CONFIGFILE

        if not self.__defaults_options:
            self.load()
            self.__defaults()
            self.__defaults_options = True

    def __defaults(self):
        """Getting or writing default configuration inside a file"""
        self.logger.info("Setting default options")
        self.get("graph", "title", "Untitled")
        self.get("graph", "type", "MultiDiGraph")
        self.get("graph", "background-color", "#FFFFFF")
        self.get("vertex", "fill-color", "#FFFFFF")
        self.get("vertex", "border-color", "#000000")
        self.get("vertex", "size", "30")
        self.get("vertex", "border-size", "2")
        self.get("vertex", "font-size", "12")
        self.get("edge", "color", "#000000")
        self.get("edge", "width", "1")

    def load(self):
        """Reads configuration"""
        self.config = ConfigParser.ConfigParser()
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

    def get(self, section, variable, default = ""):
        """Gets a variable from a section of config"""
        if not self.config.has_section(section):
            self.logger.warning("Config sections didn't exist: %s" % section)
            self.config.add_section(section)
        if not self.config.has_option(section, variable):
            self.logger.warning("Config option didn't exist: %s" % variable)
            self.config.set(section, variable, str(default))
            self.logger.warning("Config option now have value: %s" % default)

#        print "value = self.config.get(" + section + ", " + variable + ")"
        value = self.config.get(section, variable)
        

        return value

    def set(self, section, variable, value):
        """Sets a variable from a section of config"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, variable, str(value))



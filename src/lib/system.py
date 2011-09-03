#!/usr/bin/python
import sys
import os
import traceback
import struct
import time
import random
import tempfile

def get_user_name():
    """Returns current user name"""
    if get_os() == "Linux":
        return os.getenv("USER")
    else:
        return os.getenv("USERNAME")

def get_os():
    """Returns the name of the OS"""
    try:
        # quick workaround - windows has no 'uname' :)
        ret = os.uname()
        return "Linux"
    except:
        return "Windows"

def timefunc():
    # TODO: if windows, return time.clock(); otherwise return time.time()
    return time.time()

def create_tmp_file(suffix=''):
    """Creates a temporary file"""
    fd, tmpfile = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return tmpfile

def get_home():
    """Returns user homedir"""
    if get_os() == "Linux":
        return os.getenv("HOME")
    else:
        return os.getenv("HOMEPATH")

def get_system_storage():
    """Returns the directory where global configuration is located"""
    if get_os() == "Linux":
        return "/etc/"
    else:
        # where to store on windows?
        return get_local_storage(".")

def get_local_storage(directory="", create=False):
    """Returns the directory to store files locally"""
    localdir = "%s%s%s" % (get_home(), os.sep, directory)
    if create:
        if not os.access(localdir, os.W_OK | os.R_OK):
            os.makedirs(localdir)
    return localdir

def create_local_file(directory, filename):
    """Creates a new file in local storage dir"""
    localdir = get_local_storage(directory, create=True)
    return get_full_path(localdir, filename)

def get_full_path(directory, filename):
    """Gets the full path to a filename"""
    return "%s%s%s" % (directory, os.sep, filename)

def get_algorithms():
    """Gets all algorithms inside a directory"""
    path = sys.argv[0]
    path = os.path.split(path)[0]
    path = os.path.abspath(path)
    path = os.path.join(path, '..', 'algorithms')
    
    algorithms = []

    for file in os.listdir(path):
        if os.path.isdir(file):
            continue
        if file == "__init__.py" or not ".py" in file:
            continue
        
        file_name, file_ext = file.split('.')
        tmp_from = file_name
        tmp_import = underscore_to_classname(file_name)
        module = __import__(tmp_from, globals(), locals(), [tmp_import], -1)
        algorithms.append(getattr(module, tmp_import))
    
    return algorithms

def underscore_to_classname(value):
    """Convert a undercore name to classname (CamelCase)"""
    def camelcase(): 
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))



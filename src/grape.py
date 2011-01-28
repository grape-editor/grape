from gui.MainScreen import MainScreen

global _
import sys
import os
import locale
import gettext

APP_NAME = "grape"

local_path = os.path.realpath(os.path.dirname(sys.argv[0])) + "/language" 

langs = []
lc, encoding = locale.getdefaultlocale()
if (lc):
    langs = [lc]
language = os.environ.get('LANGUAGE', None)
if (language):
    langs += language.split(":")
langs += ["pt_BR", "en_US"]

gettext.bindtextdomain(APP_NAME, local_path)
gettext.textdomain(APP_NAME)
lang = gettext.translation(APP_NAME, local_path, languages=langs, fallback = True)

_ = lang.gettext

if __name__ == "__main__":
    grape = MainScreen()













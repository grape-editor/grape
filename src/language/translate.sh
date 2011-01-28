#! /bin/sh

intltool-extract --type=gettext/glade ../gui/*.ui
xgettext --language=Python --keyword=_ --keyword=N_ --output=default.pot ../*.py ../gui/*.py ../gui/*.h ../lib/*.py
msginit --input=default.pot --locale=pt_BR

mkdir -p pt_BR/LC_MESSAGES
msgfmt --output-file=pt_BR/LC_MESSAGES/grape.mo pt_BR.po



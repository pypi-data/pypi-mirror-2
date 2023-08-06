
Abstract
========

'ezodf' is a Python package to create new or open existing OpenDocumentFormat files
to extract, add, modify or delete document data.

a simple example::

    import ezodf

    ods = ezodf.ODS('testspreadsheet.ods')
	sheet = ezodf.Spreadsheet(ods, 'SHEET')
	sheet[0, 0] = ezodf.Cell("Textcell")
    ods.save()

for more examples see: /examples folder

Dependencies
============

* lxml <http://codespeak.net/lxml/> for painless serialisation with prefixe
  declaration (xlmns:prefix="global:namespace:specifier") in the root element,
  and declarations for unused prefixes are also possible.

The target platform is Python 3.1+, no Python 2 support planned at this time.

Installation
============

with pip::

    pip install ezodf

or from source::

    python setup.py install

Tests
=====

run tests ::

    python runtests.py

on Windows::

    runtests.bat

Documentation
=============

http://packages.python.org/ezodf

send feedback to mozman@gmx.at

ezodf can be found on bitbucket.org at:

http://bitbucket.org/mozman/ezodf

MM to Notes
===========

This is a simple utility to convert a FreeMind mind-map (.mm) into meeting notes
in HTML or text.
Does some XML foo to get meeting notes from your MM file.
Looks for top node called "attendees", and a node called "Action Items" and
organizes stuff under "Discussed" chronologically where we expect every top
level item to be a person's name (who said it).

Links
-----
FreeMind: http://freemind.sourceforge.net/wiki/index.php/Main_Page


Install
-------

# python setup.py install

or

# easy_install.py mm2notes

Prerequesites
-------------

Requires Python 2.3 or greater
Requires elementtree

License
-------

Apache Version 2.0

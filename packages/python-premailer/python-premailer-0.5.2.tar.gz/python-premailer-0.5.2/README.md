python-premailer
================

python-premailer converts HTML with style tags into HTML with inline style attributes; gmail won't render nice without it!

I made it so I could send colorized git diffs of func-inventory around...

Use:
    sudo pip install python-premailer

    ###

    from pypremailer import Premailer

    html = sys.stdin.read()

    premailer = Premailer(html)

    inlined_html = premailer.premail()

    print inlined_html

Get the source:

    http://github.com/ralphbean/python-premailer

On PyPI:

    http://pypi.python.org/pypi/python-premailer


Excuses, excuses
----------------
This definitely already exists in pypi under the name 'premailer', but I wanted to reimplement it without the use of lxml.

Check it out!  http://pypi.python.org/pypi/premailer

Inspired by
-----------

Emogrifier (php):  http://www.pelagodesign.com/sidecar/emogrifier/

Premailer (ruby):  http://premailer.dialect.ca/

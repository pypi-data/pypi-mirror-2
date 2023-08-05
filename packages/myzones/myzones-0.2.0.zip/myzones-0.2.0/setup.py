#!/usr/bin/env python

from distutils.core import setup
import re

NAME = 'myzones'
VER = '0.2.0'
DIR = 'myzones'
DEB_NAME = NAME.replace('-', '')
RELEASE_FILE = 'CHANGELOG.txt'
RELEASE_FORMAT=r'Version (?P<ver>[^ ]+) \((?P<date>[^)]+)\)'
DEPENDS=['pytz']
MAN_FILE='man/%s.1' % NAME

SETUP = dict(
    name = NAME,
    version = VER,
    description='Show the timezones you\'re interested in',
    long_description=
"""Show the timezones you're interested in in a dialog.

If you live in the southern hemisphere like I do, you probably constantly struggle to figure out
what time it is in the northern hemisphere.  This is because, when daylight savings time comes
around the north jumps forward and we jump back (or vice-versa).  To make things even more
complicated, the date and hour that the time changes is usually different.  There will be one or
more weeks where time difference is X hours.  Add the classic "off by one" error or a little
dyslexia and your bound to get the time wrong and wake somebody up at 8:00 in the morning.

With MyZones you configure the timezones you are most interested in and then run it.  You can go
forward or backwards in time if you are trying to schedule a date in the future, say.

A screenshot can be found here : http://myzones.googlecode.com/svn/trunk/doc/screen-shot.png

You can configure to show the timezones you are interested in.  As long as the timezone on your machine is correct and your computer's clock is on time, then it should show the right time for that timezone.  The pytz ({{{apt-get install python-tz}}} for debian users) module is very complete (and correct) even has historical timezones that don't exist anymore.

Requirements
------------

   * pytz
   * wxPython
   * Python

Configuration
-------------

Under Linux create a file called ~/.myzones.ini or ~/myzones.ini and it'll use that file for configuration.  Under Windows you would put the file it under something like 'c:\Documents and Settings\scott\My Documents'.

The configuration file looks something like this::

  [config]
  show_seconds:True
  [timezones]
  MTV: 1|US/Pacific
  Mom: 2|US/Eastern
  *Home*: 3|Brazil/East

In the config section, you can put in some configuration information, of which there is currently only one thing to configure.

For the timezones section you can give any names on the left hand side and the time zone (one of
the [http://myzones.googlecode.com/svn/trunk/doc/common_zone_names.txt Common Zone Names] ) If you
want the timezones to appear in a certain order you need to prepend the name with 1|, 2|, etc., and
is thus recommended.
""",
    author='Scott Kirkwood',
    author_email='scott@forusers.com',
    url='http://code.google.com/p/%s/' % NAME,
    download_url='http://%s.googlecode.com/files/%s-%s.zip' % (NAME, NAME, VER),
    packages=['myzones'],
    scripts=['scripts/myzones'],
    keywords=['timezones', 'utility', 'wxPython', 'python', 'pytz'],
    license='Apache 2.0',
    platforms=['POSIX', 'Windows'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)

if __name__ == '__main__':
  setup(**SETUP)

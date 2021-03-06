"""
py2app/py2exe build script for Electrum Litecoin

Usage (Mac OS X):
     python setup.py py2app

Usage (Windows):
     python setup.py py2exe
"""

import sys, os, shutil, re
from setuptools import setup
from lib.version import ELECTRUM_VERSION as version
from lib.util import print_error


name = "Electrum"
mainscript = 'electrum'

if sys.version_info[:3] < (2,6,0):
    print_error("Error: " + name + " requires Python version >= 2.6.0...")
    sys.exit(1)

if sys.platform == 'darwin':
    shutil.copy(mainscript, mainscript + '.py')
    mainscript += '.py'
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        options=dict(py2app=dict(argv_emulation=True,
                                 iconfile='electrum.icns',
                                 resources=["data", "icons"])),
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[mainscript],
    )

setup(
    name = name,
    version = version,
    **extra_options
)

if sys.platform == 'darwin':
    # Remove the copied py file
    os.remove(mainscript)
    resource = "dist/" + name + ".app/Contents/Resources/"

    # Try to locate qt_menu
    # Let's try the port version first!
    if os.path.isfile("/opt/local/lib/Resources/qt_menu.nib"):
      qt_menu_location = "/opt/local/lib/Resources/qt_menu.nib"
    else:
      # No dice? Then let's try the brew version
      qt_menu_location = os.popen("find /usr/local/Cellar -name qt_menu.nib | head").read()
      qt_menu_location = re.sub('\n','', qt_menu_location)

    if(len(qt_menu_location) == 0):
      print "Sorry couldn't find your qt_menu.nib this probably won't work"

    # Need to include a copy of qt_menu.nib
    shutil.copytree(qt_menu_location, resource + "qt_menu.nib")
    # Need to touch qt.conf to avoid loading 2 sets of Qt libraries
    fname = resource + "qt.conf"
    with file(fname, 'a'):
        os.utime(fname, None)

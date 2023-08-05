#!/usr/bin/env python

from distutils.core import setup
from MplayerCtrl import __version__

setup(name='MplayerCtrl',
      version=__version__,
      description='A wx.Panel, which wraps the Mplayer into wxPython',
      author='David Herberth',
      author_email='admin@dav1d.de',
      url='http://mplayerctrl.dav1d.de',
      py_modules=['MplayerCtrl'],
      license='MIT',
      platforms='any'
     )

#!/usr/bin/env python
# -*- Python -*-
# -*- coding: utf-8 -*-

'''install script for OpenHRIWeb

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

from setuptools import setup, find_packages
import sys, os
from openhriweb.__init__ import __version__

cmd_classes = {}
try:
    from DistUtilsExtra.command import *
    cmd_classes.update({"build": build_extra.build_extra,
                        "build_i18n" :  build_i18n.build_i18n})
except ImportError:
    pass

# vim: tw=79
if sys.platform == "win32":
    # py2exe options
    extra = {
        "console": [
            "openhriweb/JabberRTC.py",
            "openhriweb/WebServerRTC.py",
            "openhriweb.XMLtoJSONRTC.py"
            "openhriweb/Manager.py"
            ],
        "options": {
            "py2exe": {
                "includes": "xml.etree.ElementTree, lxml._elementpath, OpenRTM_aist, RTC, gzip",
                "dll_excludes": ["ierutil.dll", "powrprof.dll", "msimg32.dll", "mpr.dll", "urlmon.dll", "dnsapi.dll"],
            }
        }
    }
else:
    extra = {}

setup(name='openhriweb',
      cmdclass=cmd_classes,
      version=__version__,
      description="RT Components for web based systems (part of OpenHRI softwares)",
      long_description="""RT Components for web based systems (part of OpenHRI softwares).""",
      classifiers=[],
      keywords='',
      author='Yosuke Matsusaka',
      author_email='yosuke.matsusaka@aist.go.jp',
      url='http://openhri.net/',
      license='EPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
        ],
      entry_points="""
      [console_scripts]
      jabberrtc = openhriweb.JabberRTC:main
      webserverrtc = openhriweb.WebServerRTC:main
      xmltojsonrtc = openhriweb.XMLtoJSONRTC:main
      openhriwebmanager = openhriweb.Manager:main
      """,
      **extra
      )

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''manager for openhriweb components

Copyright (C) 2009-2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys, os, signal, time, traceback, locale, codecs
import OpenRTM_aist
import RTC

import WebServerRTC
import JabberRTC
import XMLtoJSONRTC

def MyModuleInit(manager):
    WebServerRTC.WebServerRTCInit(manager)
    JabberRTC.JabberRTCInit(manager)
    XMLtoJSONRTC.XMLtoJSONRTCInit(manager)

def main():
    locale.setlocale(locale.LC_CTYPE, '')
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = 'us-ascii'
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = 'replace')
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = 'replace')

    manager = OpenRTM_aist.Manager.init(sys.argv)
    manager.setModuleInitProc(MyModuleInit)
    manager.activateManager()
    manager.runManager()

if __name__=='__main__':
    main()

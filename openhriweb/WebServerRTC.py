#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''web based interface for controlling robot

Copyright (C) 2009-2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys
import os
import signal
import time
import traceback
import threading
import locale
import codecs
import optparse
import CGIHTTPServer
from SocketServer import ThreadingMixIn
from urlparse import urlparse
import OpenRTM_aist
import RTC
import utils
from __init__ import __version__
try:
    import gettext
    _ = gettext.translation(domain='openhriweb', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Bridge RTC data stream to HTTP protocol. By using this component you can control your robot using web browser.')

# workaround for reverse DNS lookup
def my_address_string(self):
    host, port = self.client_address[:2]
    return '%s' % host

CGIHTTPServer.CGIHTTPRequestHandler.address_string = my_address_string

class MyHTTPHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    '''HTTP request handler with RTC bridge.'''
    def do_GET(self):
        global manager
        if self.path[:5] == "/rtc/" and manager.comp:
            manager.comp.onRequest(self)
        else:
            CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        global manager
        if self.path[:5] == "/rtc/" and manager.comp:
            manager.comp.onRequest(self)
        else:
            CGIHTTPServer.CGIHTTPRequestHandler.do_POST(self)

class ThreadedHTTPServer(ThreadingMixIn, CGIHTTPServer.BaseHTTPServer.HTTPServer):
    '''Multi-threaded HTTP server.'''

WebServerRTC_spec = ["implementation_id", "WebServerRTC",
                     "type_name",         "WebServerRTC",
                     "description",       __doc__.encode('UTF-8'),
                     "version",           __version__,
                     "vendor",            "Yosuke Matsusaka, AIST",
                     "category",          "Web",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "10",
                     "language",          "Python",
                     "lang_type",         "script",
                     "conf.default.port",                 "6809",
                     "conf.__description__.port",         _("Port of HTTP server (e.g. 6809).").encode('UTF-8'),
                     "conf.default.documentroot",         ".",
                     "conf.__description__.documentroot", _("Root path of html documents (e.g. /var/www).").encode('UTF-8'),
                     "conf.__doc__.usage",         """
To run this component::

  $ webserverrtc

Examples:
 See https://github.com/yosuke/OpenHRIWeb/tree/master/examples/webserverrtc
""",
                     ""]

class WebServerRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf("WebServerRTC")
        self._logger.RTC_INFO("WebServerRTC version " + __version__)
        self._logger.RTC_INFO("Copyright (C) 2010 Yosuke Matsusaka")
        self._port = ['',]
        self._documentroot = ['',]
        self._httpd = None

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        # bind configuration parameters
        self.bindParameter('port', self._port, '6809')
        self.bindParameter('documentroot', self._documentroot, '.')
        self._indata = RTC.TimedString(RTC.Time(0,0), "")
        self._inport = OpenRTM_aist.InPort("indata", self._indata)
        self._inport.appendProperty('description', _('Text message to be accessed via url [/rtc/indata] using javascript code.').encode('UTF-8'))
        self.registerInPort(self._inport._name, self._inport)
        self._outdata = RTC.TimedString(RTC.Time(0,0), "")
        self._outport = OpenRTM_aist.OutPort("outdata", self._outdata)
        self._outport.appendProperty('description', _('Text message to be accessed via url [/rtc/outdata] using javascript code.').encode('UTF-8'))
        self.registerOutPort(self._outport._name, self._outport)
        self._logger.RTC_INFO('component created')
        return RTC.RTC_OK
    
    def onActivated(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onActivated(self, ec_id)
        os.chdir(self._documentroot[0])
        self._httpd = ThreadedHTTPServer(("", int(self._port[0])), MyHTTPHandler)
        return RTC.RTC_OK

    def onRequest(self, s):
        p = urlparse(s.path)
        if p.path == "/rtc/indata":
            self._logger.RTC_INFO('reading data from inport... ')
            while not self._inport.isNew():
                time.sleep(0.1)
            data = self._inport.read().data
            #if self._inport.isNew():
            #    data = self._inport.read().data
            #else:
            #    data = ""
            self._logger.RTC_INFO("read data from inport: %s"  % (data,))
            self._logger.RTC_INFO("sending data to the client... ")
            try:
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write(data)
                self._logger.RTC_INFO("done")
            except:
                self._logger.RTC_WARN("write error (probably the client has timed out)")
        elif p.path == "/rtc/outdata":
            self._outdata.data = p.query
            self._outport.write()
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("OK")
            self._logger.RTC_INFO("write data to outport: %s"  % (p.query,))

    def onExecute(self, ec_id):
        self._httpd.handle_request()
        return RTC.RTC_OK
    
    def onDeactivate(self, ec_id):
        if self._httpd:
            self._httpd.shutdown()
            self._httpd = None
        return RTC.RTC_OK

    def onFinalize(self):
        if self._httpd:
            self._httpd.shutdown()
            self._httpd = None
        return RTC.RTC_OK

def WebServerRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=WebServerRTC_spec)
    manager.registerFactory(profile, WebServerRTC, OpenRTM_aist.Delete)

def MyModuleInit(manager):
    WebServerRTCInit(manager)
    comp = manager.createComponent('WebServerRTC')

def main():
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")
    
    parser = utils.MyParser(version=__version__, description=__doc__)
    utils.addmanageropts(parser)
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
    manager.setModuleInitProc(MyModuleInit)
    manager.activateManager()
    manager.runManager()

if __name__=='__main__':
    main()

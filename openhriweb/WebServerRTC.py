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

import sys, signal, time, traceback, threading
import CGIHTTPServer
from SocketServer import ThreadingMixIn
from urlparse import urlparse
import OpenRTM_aist
import RTC

httpport = 6809

# signal handler
def myhandler(code, val):
    global httpd, mainloop
    print 'terminating...'
    mgr = OpenRTM_aist.Manager.instance()
    mgr.terminate()
    #httpd.shutdown()
    #exit()
    mainloop = False

def my_address_string(self):
    host, port = self.client_address[:2]
    return '%s' % host

CGIHTTPServer.CGIHTTPRequestHandler.address_string = my_address_string

class MyHTTPHandler(CGIHTTPServer.CGIHTTPRequestHandler):
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
    """Handle requests in a separate thread."""

WebServerRTC_spec = ["implementation_id", "WebServerRTC",
                     "type_name",         "WebServerRTC",
                     "description",       "Web Server Component",
                     "version",           "1.0.0",
                     "vendor",            "Yosuke Matsusaka, AIST",
                     "category",          "Web",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "10",
                     "language",          "Python",
                     "lang_type",         "script",
                     ""]

class WebServerRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        try:
            OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
            self._indata = RTC.TimedString(RTC.Time(0,0), "")
            self._inport = OpenRTM_aist.InPort("indata", self._indata)
            self.registerInPort("indata", self._inport)
            self._outdata = RTC.TimedString(RTC.Time(0,0), "")
            self._outport = OpenRTM_aist.OutPort("outdata", self._outdata)
            self.registerOutPort("outdata", self._outport)
            print "component created"
        except:
            print traceback.format_exc()
    
    def onRequest(self, s):
        try:
            p = urlparse(s.path)
            if p.path == "/rtc/indata":
                print "reading data from inport... "
                while not self._inport.isNew():
                    time.sleep(0.1)
                data = self._inport.read().data
                #if self._inport.isNew():
                #    data = self._inport.read().data
                #else:
                #    data = ""
                print "read data from inport: %s"  % (data,)
                print "sending data to the client... "
                try:
                    s.send_response(200)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                    s.wfile.write(data)
                    print "done"
                except:
                    print "write error (probably the client has timed out"
            elif p.path == "/rtc/outdata":
                self._outdata.data = p.query
                self._outport.write()
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write("OK")
                print "write data to outport: %s"  % (p.query,)
        except:
            print traceback.format_exc()

    def onExecute(self, ec_id):
        time.sleep(1)
        return RTC.RTC_OK

class WebServerRTCManager:
    def __init__(self):
        self.comp = None
        self.manager = OpenRTM_aist.Manager.init(sys.argv)
        self.manager.setModuleInitProc(self.moduleInit)
        self.manager.activateManager()

    def start(self):
        self.manager.runManager(True)

    def moduleInit(self, manager):
        try:
            profile=OpenRTM_aist.Properties(defaults_str=WebServerRTC_spec)
            manager.registerFactory(profile, WebServerRTC, OpenRTM_aist.Delete)
            self.comp = manager.createComponent("WebServerRTC?exec_cxt.periodic.rate=1")
        except:
            print traceback.format_exc()

def main():
    global manager, httpd, mainloop
    mainloop = True
    manager = None
    httpd = None
    manager = WebServerRTCManager()
    manager.start()
    httpd = ThreadedHTTPServer(("", httpport), MyHTTPHandler)
    signal.signal(signal.SIGINT, myhandler)
    #httpd.serve_forever()
    while mainloop:
        httpd.handle_request()

if __name__=='__main__':
    main()

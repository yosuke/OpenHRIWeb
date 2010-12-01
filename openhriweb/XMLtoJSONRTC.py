#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''XML to JSON conversion component

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import os, sys, time, traceback, getopt
import lxml
import lxml.objectify
import simplejson as json
import OpenRTM_aist
import RTC

# the objectJSONEncoder class (thanks to Anton I. Sipos, http://gist.github.com/345559):
class objectJSONEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o, lxml.objectify.IntElement):
            return int(o)
        if isinstance(o, lxml.objectify.NumberElement) or isinstance(o, lxml.objectify.FloatElement):
            return float(o)
        if isinstance(o, lxml.objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            return o.__dict__
        return json.JSONEncoder.default(self, o)

XMLtoJSONRTC_spec = ["implementation_id", "XMLtoJSONRTC",
                     "type_name",         "XMLtoJSONRTC",
                     "description",       "XML to JSON conversion component (python implementation)",
                     "version",           "1.0.0",
                     "vendor",            "AIST",
                     "category",          "communication",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "10",
                     "language",          "Python",
                     "lang_type",         "script",
                     ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class XMLtoJSONRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        try:
            OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        except:
            print traceback.format_exc()

    def onInitialize(self):
        try:
            self._transform = objectJSONEncoder()
            # create inport
            self._indata = RTC.TimedString(RTC.Time(0,0), "")
            self._inport = OpenRTM_aist.InPort("text", self._indata)
            self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                                  DataListener("ON_BUFFER_WRITE", self))
            self.registerInPort("text", self._inport)
            # create outport
            self._outdata = RTC.TimedString(RTC.Time(0,0), "")
            self._outport = OpenRTM_aist.OutPort("result", self._outdata)
            self.registerOutPort("result", self._outport)
        except:
            print traceback.format_exc()
        return RTC.RTC_OK
    
    def onData(self, name, data):
        try:
            udoc = lxml.objectify.fromstring(data.data)
            self._outdata.data = self._transform.encode(udoc)
            self._outport.write(self._outdata)
            print self._outdata.data
        except:
            print traceback.format_exc()

    def onExecute(self, ec_id):
        time.sleep(1)
        return RTC.RTC_OK

class XMLtoJSONRTCManager:
    def __init__(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "adlf:o:p:h", ["help",])
        except getopt.GetoptError:
            usage()
            sys.exit()
        managerargs = [sys.argv[0]]
        for o, a in opts:
            if o in ("-a", "-d", "-l"):
                managerargs.append(o)
            if o in ("-f", "-o", "-p"):
                managerargs.append(o, a)
            if o in ("-h", "--help"):
                usage()
                sys.exit()
        self._files = args
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(managerargs)
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=XMLtoJSONRTC_spec)
        manager.registerFactory(profile, XMLtoJSONRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("XMLtoJSONRTC?exec_cxt.periodic.rate=1")

def usage():
    print "usage: %s [-f rtc.conf] [--help]" % (os.path.basename(sys.argv[0]),)

def main():
    manager = XMLtoJSONRTCManager()
    manager.start()

if __name__=='__main__':
    main()

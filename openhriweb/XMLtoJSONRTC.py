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

import os
import sys
import time
import traceback
import getopt
import locale
import codecs
import lxml
import lxml.objectify
import simplejson as json
import OpenRTM_aist
import RTC
import utils
from __init__ import __version__
try:
    import gettext
    _ = gettext.translation(domain='openhriweb', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('XML to JSON conversion component')

# the objectJSONEncoder class
# (thanks to Anton I. Sipos, http://gist.github.com/345559):
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
                     "description",       __doc__.encode('UTF-8'),
                     "version",           __version__,
                     "vendor",            "AIST",
                     "category",          "communication",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "10",
                     "language",          "Python",
                     "lang_type",         "script",
                     "conf.__doc__.usage",         """
To run this component::

  $ xmltojsonrtc
""",
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
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf("XMLtoJSONRTC")
        self._logger.RTC_INFO("XMLtoJSONRTC version " + __version__)
        self._logger.RTC_INFO("Copyright (C) 2010 Yosuke Matsusaka")

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        self._transform = objectJSONEncoder()
        # create inport
        self._indata = RTC.TimedString(RTC.Time(0,0), "")
        self._inport = OpenRTM_aist.InPort("text", self._indata)
        self._inport.appendProperty('description', _('Input text in XML format.').encode('UTF-8'))
        self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                              DataListener("ON_BUFFER_WRITE", self))
        self.registerInPort(self._inport._name, self._inport)
        # create outport
        self._outdata = RTC.TimedString(RTC.Time(0,0), "")
        self._outport = OpenRTM_aist.OutPort("result", self._outdata)
        self._outport.appendProperty('description', _('Output text in JSON format.').encode('UTF-8'))
        self.registerOutPort(self._inport._name, self._outport)
        return RTC.RTC_OK
    
    def onData(self, name, data):
        udoc = lxml.objectify.fromstring(data.data)
        self._outdata.data = self._transform.encode(udoc)
        self._outport.write(self._outdata)
        self._logger.RTC_INFO(self._outdata.data)

def XMLtoJSONRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=XMLtoJSONRTC_spec)
    manager.registerFactory(profile, XMLtoJSONRTC, OpenRTM_aist.Delete)

def MyModuleInit(manager):
    XMLtoJSONRTCInit(manager)
    comp = manager.createComponent('XMLtoJSONRTC')

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
        return 1

    manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
    manager.setModuleInitProc(MyModuleInit)
    manager.activateManager()
    manager.runManager()
    return 0

if __name__=='__main__':
    sys.exit(main())



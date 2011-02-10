#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Jabber(XMPP) messaging component

Copyright (C) 2010
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
import locale
import codecs
import traceback
import OpenRTM_aist
import RTC
from pyxmpp.all import JID, Message
from pyxmpp.jabber.client import JabberClient
from pyxmpp.streamtls import TLSSettings
import optparse
import utils
from __init__ import __version__
try:
    import gettext
    _ = gettext.translation(domain='openhriweb', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Bridge RTC data stream to Jabber(XMPP) message. By using this component you can send and receive messages to Jabber clients (e.g. google talk) from your robot.')

class Client(JabberClient):
    def __init__(self, jid, password, obj):
        if not jid.resource:
            jid = JID(jid.node, jid.domain, "JabberRTC")
        tls = TLSSettings(require = True, verify_peer = False)
        auth = ['sasl:PLAIN']
        JabberClient.__init__(self, jid, password, tls_settings = tls, auth_methods = auth)
        self._rtobj = obj

    def session_started(self):
        JabberClient.session_started(self)
        self.stream.set_presence_handler(None, self.presence)
        self.stream.set_presence_handler("unavailable", self.presence)
        self.stream.set_presence_handler("subscribe", self.presence_control)
        self.stream.set_presence_handler("subscribed", self.presence_control)
        self.stream.set_presence_handler("unsubscribe", self.presence_control)
        self.stream.set_presence_handler("unsubscribed", self.presence_control)
        self.stream.set_message_handler("normal",self.message)

    def message(self, stanza):
        f = stanza.get_from().as_unicode()
        body = stanza.get_body()
        if body is not None:
            self._rtobj._logger.RTC_INFO(u'%s has send you message: %s' % (f, body))
            self._rtobj._outdata.data[0] = body
            self._rtobj._outdata.data[1] = f
            self._rtobj._outport.write()

    def sendmessage(self, to, body):
        self._rtobj._logger.RTC_INFO(u'send message to %s: %s' % (to, body))
        self.stream.send(Message(to_jid = JID(to), body = body))

    def presence(self, stanza):
        f = stanza.get_from().as_unicode()
        state = "available"
        if stanza.get_type() == "unavailable":
            state = "unavailable"
        if stanza.get_show() == "away":
            state = "away"
        self._rtobj._logger.RTC_INFO(u"%s has become %s" % (f, state))
        self._rtobj._statedata.data[0] = state
        self._rtobj._statedata.data[1] = f
        self._rtobj._stateport.write()

    def presence_control(self,stanza):
        return stanza.make_accept_response()


JabberRTC_spec = ["implementation_id", "JabberRTC",
                  "type_name",         "JabberRTC",
                  "description",       __doc__.encode('UTF-8'),
                  "version",           __version__,
                  "vendor",            "AIST",
                  "category",          "communication",
                  "activity_type",     "DataFlowComponent",
                  "max_instance",      "10",
                  "language",          "Python",
                  "lang_type",         "script",
                  "conf.default.id",               "[your id]@gmail.com",
                  "conf.__description__.id",       _("Id of your Jabber account (e.g. john.doe@example.com).").encode('UTF-8'),
                  "conf.default.password",         "[your password]",
                  "conf.__description__.password", _("Password of your Jabber account.").encode('UTF-8'),
                  "conf.__doc__.usage",         """
To run this component::

  $ jabberrtc

Examples:
 See https://github.com/yosuke/OpenHRIWeb/tree/master/examples/jabberrtc
""",
                  ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedStringSeq(RTC.Time(0,0),[]))
        self._obj.onData(self._name, data)

class JabberRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf("JabberRTC")
        self._logger.RTC_INFO("JabberRTC version " + __version__)
        self._logger.RTC_INFO("Copyright (C) 2010 Yosuke Matsusaka")
        self._c = None
        self._jid = ['',]
        self._password = ['',]

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        # bind configuration parameters
        self.bindParameter('id', self._jid, '[your id]@gmail.com')
        self.bindParameter('password', self._password, '[your password]')
        # create inport
        self._indata = RTC.TimedStringSeq(RTC.Time(0,0), [])
        self._inport = OpenRTM_aist.InPort('text', self._indata)
        self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                              DataListener('ON_BUFFER_WRITE', self))
        self._inport.appendProperty('description', _('Message in TimedStringSeq format (["message body", "addressee1", "adressee2",...]').encode('UTF-8'))
        self.registerInPort(self._inport._name, self._inport)
        # create outport for message
        self._outdata = RTC.TimedStringSeq(RTC.Time(0,0), [])
        self._outport = OpenRTM_aist.OutPort('message', self._outdata)
        self._outport.appendProperty('description', _('Message in TimedStringSeq format (["message body", "from"]').encode('UTF-8'))
        self.registerOutPort(self._outport._name, self._outport)
        # create outport for status
        self._statedata = RTC.TimedStringSeq(RTC.Time(0,0), [])
        self._stateport = OpenRTM_aist.OutPort('status', self._statedata)
        self._stateport.appendProperty('description', _('Status in TimedStringSeq format (["status", "from"]').encode('UTF-8'))
        self.registerOutPort(self._stateport._name, self._stateport)
        return RTC.RTC_OK

    def onActivated(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onActivated(self, ec_id)
        self._c = Client(JID(self._jid[0]), self._password[0], self)
        self._c.connect()
        return RTC.RTC_OK
    
    def onDeactivate(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onDeactivate(self, ec_id)
        if self._c:
            self._c.disconnect()
            self._c = None
        return RTC.RTC_OK

    def onData(self, name, data):
        body = data.data[0]
        for to in data.data[1:]:
            self._c.sendmessage(to, body)

    def onResult(self, data):
        pass
    
    def onExecute(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onExecute(self, ec_id)
        if self._c:
            self._c.loop(1)
        return RTC.RTC_OK

    def onFinalize(self):
        OpenRTM_aist.DataFlowComponentBase.onFinalize(self)
        if self._c:
            self._c.disconnect()
            self._c = None
        return RTC.RTC_OK

def JabberRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=JabberRTC_spec)
    manager.registerFactory(profile, JabberRTC, OpenRTM_aist.Delete)

def MyModuleInit(manager):
    JabberRTCInit(manager)
    comp = manager.createComponent('JabberRTC')

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

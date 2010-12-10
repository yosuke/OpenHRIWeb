JabberRTC0.rtc
==============
Jabber(XMPP) messaging component (python implementation)

:Vendor: AIST
:Version: 1.0.0
:Category: communication
:License: EPL
:Contact: Yosuke Matsusaka <yosuke.matsusaka@aist.go.jp>
:URL: http://openhri.net/

Introduction
------------

Bridge RTC data stream to Jabber(XMPP) message. By using this component
you can send and receive messages to Jabber clients (e.g. google talk) from
your robot.

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedStringSeq", "Message in TimedStringSeq format (['message body', 'addressee1', 'adressee2',...]"
   "message", "DataOutPort", "TimedStringSeq", "Message in TimedStringSeq format (['message body', 'from']"
   "status", "DataOutPort", "TimedStringSeq", "Status in TimedStringSeq format (['status', 'from']"

Configuration parameters
------------------------
.. csv-table:: Configration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "password", "Password of your Jabber account."
   "id", "Id of your Jabber account (e.g. john.doe@example.com)."

Usage
-----

To run this component:
 $ jabberrtc

Examples:
 See https://github.com/yosuke/OpenHRIWeb/tree/master/examples/jabberrtc


WebServerRTC0.rtc
=================
Web server component

:Vendor: Yosuke Matsusaka, AIST
:Version: 1.0.0
:Category: Web
:License: EPL
:Contact: Yosuke Matsusaka <yosuke.matsusaka@aist.go.jp>
:URL: http://openhri.net/

Introduction
============

Bridge RTC data stream to HTTP protocol. By using this component you can
control your robot using web browser.

Usage
=====

To run this component:
 $ webserverrtc

Examples:
 See https://github.com/yosuke/OpenHRIWeb/tree/master/examples/webserverrtc

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "indata", "DataInPort", "TimedString", "Text message to be accessed via url [/rtc/indata] using javascript code."
   "outdata", "DataOutPort", "TimedString", "Text message to be accessed via url [/rtc/outdata] using javascript code."

Configuration parameters
------------------------
.. csv-table:: Configration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "port", "Port of HTTP server (e.g. 6809)."
   "documentroot", "Root path of html documents (e.g. /var/www)."


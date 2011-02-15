WebServerRTC
============
Bridge RTC data stream to HTTP protocol. By using this component you can control your robot using web browser.

:Vendor: Yosuke Matsusaka, AIST
:Version: 1.00
:Category: Web

Usage
-----

To run this component::

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

.. digraph:: comp

   rankdir=LR;
   WebServerRTC [shape=Mrecord, label="WebServerRTC"];
   indata [shape=plaintext, label="indata"];
   indata -> WebServerRTC;
   outdata [shape=plaintext, label="outdata"];
   WebServerRTC -> outdata;

Configuration parameters
------------------------
.. csv-table:: Configuration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "port", "Port of HTTP server (e.g. 6809)."
   "documentroot", "Root path of html documents (e.g. /var/www)."


XMLtoJSONRTC
============
XML to JSON conversion component

:Vendor: AIST
:Version: 1.00
:Category: communication

Usage
-----

To run this component::

  $ xmltojsonrtc

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedString", "Input text in XML format."
   "result", "DataOutPort", "TimedString", "Output text in JSON format."

.. digraph:: comp

   rankdir=LR;
   XMLtoJSONRTC [shape=Mrecord, label="XMLtoJSONRTC"];
   text [shape=plaintext, label="text"];
   text -> XMLtoJSONRTC;
   result [shape=plaintext, label="result"];
   XMLtoJSONRTC -> result;


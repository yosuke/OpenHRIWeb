XMLtoJSONRTC
============
XMLからJSON形式に変換するコンポーネント

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
   
   "text", "DataInPort", "TimedString", "XML形式の入力テキスト"
   "result", "DataOutPort", "TimedString", "JSON形式の出力テキスト"

.. digraph:: comp

   rankdir=LR;
   XMLtoJSONRTC [shape=Mrecord, label="XMLtoJSONRTC"];
   text [shape=plaintext, label="text"];
   text -> XMLtoJSONRTC;
   result [shape=plaintext, label="result"];
   XMLtoJSONRTC -> result;


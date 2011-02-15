WebServerRTC
============
RTCデータストリームをHTTPプロトコルに変換するコンポーネントです。このコンポーネントを使うことで、ロボットをウェブブラウザを使って操作することが可能になります。

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
   
   "indata", "DataInPort", "TimedString", "javascriptを使ってURL [/rtc/indata] からアクセス可能になるテキストデータ"
   "outdata", "DataOutPort", "TimedString", "javascriptを使ってURL [/rtc/outdata] からアクセス可能になるテキストデータ"

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
   
   "port", "HTTPサーバのポート（例：6809）"
   "documentroot", "htmlドキュメントへのパス（例: /var/www）"


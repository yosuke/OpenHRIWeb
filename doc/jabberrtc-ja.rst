JabberRTC
=========
RTCデータストリームをJabber(XMPP)メッセージに変換するコンポーネント。このコンポーネントを使うことでロボットからJabberクライアント（google talkなど）へメッセージを送ることが可能になります。

:Vendor: AIST
:Version: 1.00
:Category: communication

Usage
-----

To run this component::

  $ jabberrtc

Examples:
 See https://github.com/yosuke/OpenHRIWeb/tree/master/examples/jabberrtc

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedStringSeq", "TimedStringSeq形式のメッセージ（['メッセージ本文', '宛先1', '宛先2', ...]）"
   "message", "DataOutPort", "TimedStringSeq", "TimedStringSeq形式のメッセージ（['メッセージ本文', '送信元']）"
   "status", "DataOutPort", "TimedStringSeq", "TimedStringSeq形式の状態情報（['状態', 'アカウント名']）"

.. digraph:: comp

   rankdir=LR;
   JabberRTC [shape=Mrecord, label="JabberRTC"];
   text [shape=plaintext, label="text"];
   text -> JabberRTC;
   message [shape=plaintext, label="message"];
   JabberRTC -> message;
   status [shape=plaintext, label="status"];
   JabberRTC -> status;

Configuration parameters
------------------------
.. csv-table:: Configuration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "password", "あなたのJabberアカウントのパスワード"
   "id", "あなたのJabberアカウントのID（例: john.doe@example.com）"


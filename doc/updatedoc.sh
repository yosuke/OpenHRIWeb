#!/bin/sh

rtexit /localhost/`hostname`.host_cxt/JabberRTC0.rtc
LANG=C jabberrtc &
sleep 2
rtdoc --format=rst --graph /localhost/`hostname`.host_cxt/JabberRTC0.rtc > jabberrtc.rst
rtexit /localhost/`hostname`.host_cxt/JabberRTC0.rtc
sleep 1
LANG=ja_JP.UTF-8 jabberrtc &
sleep 2
rtdoc --format=rst --graph /localhost/`hostname`.host_cxt/JabberRTC0.rtc > jabberrtc-ja.rst
rtexit /localhost/`hostname`.host_cxt/JabberRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/WebServerRTC0.rtc
LANG=C webserverrtc &
sleep 2
rtdoc --format=rst --graph /localhost/`hostname`.host_cxt/WebServerRTC0.rtc > webserverrtc.rst
rtexit /localhost/`hostname`.host_cxt/WebServerRTC0.rtc
sleep 1
LANG=ja_JP.UTF-8 webserverrtc &
sleep 2
rtdoc --format=rst --graph /localhost/`hostname`.host_cxt/WebServerRTC0.rtc > webserverrtc-ja.rst
rtexit /localhost/`hostname`.host_cxt/WebServerRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc
LANG=C xmltojsonrtc &
sleep 2
rtdoc --format=rst --graph /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc > xmltojsonrtc.rst
rtexit /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc
sleep 1
LANG=ja_JP.UTF-8 xmltojsonrtc &
sleep 2
rtdoc --format=rst --graph /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc > xmltojsonrtc-ja.rst
rtexit /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc

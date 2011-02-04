#!/bin/sh

rtexit /localhost/`hostname`.host_cxt/JabberRTC0.rtc
jabberrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/JabberRTC0.rtc > jabberrtc.rst
rtexit /localhost/`hostname`.host_cxt/JabberRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/WebServerRTC0.rtc
webserverrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/WebServerRTC0.rtc > webserverrtc.rst
rtexit /localhost/`hostname`.host_cxt/WebServerRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc
xmltojsonrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc > xmltojsonrtc.rst
rtexit /localhost/`hostname`.host_cxt/XMLtoJSONRTC0.rtc

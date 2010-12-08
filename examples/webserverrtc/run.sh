#!/bin/sh

RTC_PATH="/localhost/`hostname`.host_cxt/WebServerRTC0.rtc"

webserverrtc &

rtact $RTC_PATH

echo "open url http://localhost:6809/sample.html with your browser"

rtinject -n 100 -c 'RTC.TimedString({time}, "hello world")' $RTC_PATH:text

rtdel $RTC_PATH

#!/bin/sh

RTC_PATH="/localhost/`hostname`.host_cxt/JabberRTC0.rtc"

jabberrtc &

echo -n "Your Jabber ID? : "
read jid

echo -n "Your Jabber password : "
read pass

echo -n "Destination Jabber ID : "
read sid

rtconf $RTC_PATH set id $jid
rtconf $RTC_PATH set password $pass

rtact $RTC_PATH

rtinject $RTC_PATH:text 'RTC.TimedStringSeq({time}, ["hello world", "$sid"])'

rtdel $RTC_PATH

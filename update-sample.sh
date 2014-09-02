#!/usr/bin/env bash


# rss, 2min
if [ ! -f rss.txt ] || [ `find "rss.txt" -mmin +2 2>/dev/null` ]; then
    python rss.py > rss.txt
fi


# gmail, 10min
if [ ! -f gmail.txt ] || [ `find "gmail.txt" -mmin +10 2>/dev/null` ]; then
    python gmail.py > gmail.txt
fi


# weather, 30min
if [ ! -f weather.txt ] || [ `find "weather.txt" -mmin +30 2>/dev/null` ]; then
    python weather.py > weather.txt
fi


# ip, 6h
if [ ! -f myip.txt ] || [ `find "myip.txt" -mmin +360 2>/dev/null` ]; then
    python myip.py > myip.txt
fi


echo IP: `cat myip.txt`
echo rss: `cat rss.txt`
echo gmail: `cat gmail.txt`
echo weather: `cat weather.txt`

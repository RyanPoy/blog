#!/bin/sh

ps aux | grep python3 | fgrep blog_app | awk '{print "kill -9", $2}' | sh

sleep 2

cd  /data/apps/blog/current
python3 blog_app.py --port=8001 --tmpl=default --debug=false --admin_port=8000 >> /data/apps/blog.8001.log &
python3 blog_app.py --port=8002 --tmpl=default --debug=false  >> /data/apps/blog.8002.log &


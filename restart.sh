# !/bin/sh
ps aux|grep proxy.ini|grep -v grep|cut -c 9-15|xargs kill -s 9
setsid nohup uwsgi beauty.ini &
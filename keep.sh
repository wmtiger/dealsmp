#!/bin/bash
echo $$ > pid

prog=dealerclient.py
num=0
startsum=0
killsum=0

while true; do
    # chk any prog you need has closed
    num=`ps aux | grep ${prog} | grep -v grep | wc -l`
    echo 'num is '$num
    if [ ${num} -lt 1 ]; then
        echo "["`date`"]" ${prog} " has closed, startup again!"
        startsum=`expr $startsum + 1`
        nohup python /home/pi/work/dealsmp/dealerclient.py &
#    elif [ ${num} -gt 1 ]; then
#        echo "["`date`"]" ${prog} " has too more, kill all!"
#        killsum=`expr $killsum + 1`
#        killall -9 dealerclient.py
#        nohup python /home/pi/work/dealsmp/dealerclient.py &
    fi
    sleep 5
done

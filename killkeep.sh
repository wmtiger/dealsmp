#!/bin/bash
########################
#File Name:killkeep.sh
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-29 15:05:14
########################

a=""
while read line; do
    if [ "$line"x != "$a"x ]; then
        echo $line "will killed!"
        kill -9 $line
        echo '' > pid
    elif [ "$line"x = "$a"x ]; then
        echo "no pid was run!"
    fi
done < pid.log


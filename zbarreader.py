#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:zbarreader.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-07 01:45:26
########################

import picamera
import time
import io
import zbar
from PIL import Image

def scanQR(sleeptime):
    stream = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with picamera.PiCamera() as c:
#       c.resolution = (640, 480)
        c.start_preview()
        time.sleep(sleeptime)
        c.capture(stream, format='jpeg')
        stream.seek(0)
        pim = Image.open(stream).convert('L')
        w, h = pim.size
        raw = pim.tostring()
        zim = zbar.Image(w,h,'Y800', raw)
        sc.scan(zim)
        data = []
        for sb in zim:
            data.append(sb.data)
        del(zim)

        news_ids = []
        dataLen = len(data)
        for i in range(0, dataLen):
            if data[i] not in news_ids:
                news_ids.append(data[i])
        return news_ids

def getHandsQR(times=5):
    n = times
    data = scanQR(0.4)
    while times > 0:
        if len(data) >= 2:
            break
        data = scanQR(0.6)
        times -= 1
    print n - times
    return data

def getFlopQR(times=5):
    n = times
    data = scanQR(0.6)
    while times > 0:
        if len(data) >= 3:
            break
        data = scanQR(1)
        times -= 1
    print n - times
    return data

def getTurnQR(times=5):
    n = times
    data = scanQR(0.6)
    while times > 0:
        if len(data) >= 4:
            break
        data = scanQR(1)
        times -= 1
    print n - times
    return data

def getRiverQR(times=5):
    n = times
    data = scanQR(0.6)
    while times > 0:
        if len(data) >= 5:
            break
        data = scanQR(1)
        times -= 1
    print n - times
    return data

if __name__ == '__main__':
#    print getFlopQR()
#    print getTurnQR()
    print getRiverQR()
#    print getHandsQR()

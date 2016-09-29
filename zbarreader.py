#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def scanQR(sleeptime=0.5,type = 0):
    stream = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with picamera.PiCamera() as c:
        c.resolution = (2560, 1440)
        c.start_preview()
        time.sleep(sleeptime)
        c.capture(stream, format='jpeg')
        stream.seek(0)
        pim = Image.open(stream).convert('L')
 #       pim.save("t1.jpg")
        w, h = pim.size
        if type == 0:
            box = (0,0,w, h)
            #box = (w/5,0,w/4 * 3, h)
        else:
            box = (w/4,h/8,w/4 * 3, h/2)
        cpim = pim.crop(box)
#        cpim.save("test1.jpg")
        cw, ch = cpim.size
        raw = cpim.tostring()
        zim = zbar.Image(cw, ch,'Y800', raw)
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
        print news_ids
        return news_ids

def getHandQR(times=50):
    n = times
    data = scanQR(0.4)
    while times > 0:
        if len(data) >= 2:
            break
        data = scanQR(0.6, 0)
        times -= 1
    print n - times
    return data

def getFlopQR(times=50):
    n = times
    data = scanQR(0.4,1)
    while times > 0:
        if len(data) >= 3:
            break
        data = scanQR(1)
        times -= 1
    print n - times
    return data

def getTurnQR(times=50):
    n = times
    data = scanQR(0.4,2)
    while times > 0:
        if len(data) >= 4:
            break
        data = scanQR(1)
        times -= 1
    print n - times
    return data

def getRiverQR(times=50):
    n = times
    data = scanQR(0.4,3)
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
#    print getRiverQR()
    print getHandQR()


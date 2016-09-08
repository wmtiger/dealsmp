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

def scanQR():
    stream = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with picamera.PiCamera() as c:
#       c.resolution = (640, 480)
        c.start_preview()
        time.sleep(0.4)
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
        for card in data:
            if card not in news_ids:
                news_ids.append(card)
        return news_ids

def getHandsQR():
    data = scanQR()
    while 1:
        if len(data) >= 2:
            break
        data = scanQR()
    return data

def getFlopQR():
    data = scanQR()
    while 1:
        if len(data) >= 3:
            break
        data = scanQR()
    return data

def getTurnQR():
    data = scanQR()
    while 1:
        if len(data) >= 4:
            break
        data = scanQR()
    return data

def getRiverQR():
    data = scanQR()
    while 1:
        if len(data) >= 5:
            break
        data = scanQR()
    return data

if __name__ == '__main__':
    print getQR()

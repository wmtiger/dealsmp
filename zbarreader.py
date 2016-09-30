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

def deleteDuplicate(data):
    news_ids = []
    dataLen = len(data)
    for i in range(0, dataLen):
        if data[i] not in news_ids:
            news_ids.append(data[i])
    return news_ids

def scanLeft(sc, im, type):
    w,h = im.size
    if type == 0:
        box = (0,0,w/2,h)
    elif type == 1:
        box = (0,0,w/5*2,h)
    return readQR(box, sc, im, type, 'left')

def scanMiddle(sc, im, type):
    w,h = im.size
    if type == 1:
        box = (w/3,0,w/3*2,h)
    return readQR(box, sc, im, type, 'middle')

def scanRight(sc, im, type):
    w,h = im.size
    if type == 0:
        box = (w/2,0,w,h)
    elif type == 1:
        box = (w/5*3,0,w,h)
    return readQR(box, sc, im, type, 'right')

def readQR(box, sc, im, type, name):
    temp = ("hand", "flop", "turn", "river")
    lfim = im.crop(box)
    #lfim.save(temp[type]+"_"+name+".jpg")
    iw,ih = lfim.size
    lfraw = lfim.tostring()
    lfzim = zbar.Image(iw,ih,'Y800',lfraw)
    sc.scan(lfzim)
    data = []
    for sb in lfzim:
        data.append(sb.data)
    del(lfzim)
    return deleteDuplicate(data)

def scanQR(sleeptime=0.5,type = 0):
    stream = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    if type == 0:
        resolution = (800,600)
    else:
        resolution = (2400, 1800)
    with picamera.PiCamera() as c:
        c.resolution = resolution
        c.start_preview()
        time.sleep(sleeptime)
        c.capture(stream, format='jpeg')
        c.stop_preview()
        stream.seek(0)
        with Image.open(stream).convert('L') as pim:
#        pim = Image.open(stream).convert('L')
 #       pim.save("t1.jpg")
            w, h = pim.size
            cards = []
            if type == 0:
#                box = (0,0,w, h)
                #pim.save('hand.jpg')
                lfarr = scanLeft(sc, pim, type)
                rgarr = scanRight(sc, pim, type)
                if len(lfarr) > 0:
                    cards.append(lfarr[0])
                if len(rgarr) > 0:
                    cards.append(rgarr[0])
            else:
                cutLeft = w/4
                cutRight = w/4*3
                cutTop = 0
                cutBottom = h/2-h/4
                box = (cutLeft,cutTop,cutRight, cutBottom)
                ggpim = pim.crop(box)
                #ggpim.save('ggp.jpg')
                if type == 1:
                    box = (cutLeft,cutTop,cutRight-((cutRight-cutLeft)/5*2), cutBottom)
                    cpim = pim.crop(box)
                    lfarr = scanLeft(sc, cpim, type)
                    mdarr = scanMiddle(sc, cpim, type)
                    rgarr = scanRight(sc, cpim, type)
                    if len(lfarr) > 0:
                        cards.append(lfarr[0])
                    if len(mdarr) > 0:
                        cards.append(mdarr[0])
                    if len(rgarr) > 0:
                        cards.append(rgarr[0])
                else:
                    box = (0,0,ggpim.size[0],ggpim.size[1])
                    cards = readQR(box,sc,ggpim,type,'')

    print cards
    return cards

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
    t = time.time()
#    print getFlopQR()
#    print getTurnQR()
#    print getRiverQR()
    print getHandQR()
    print time.time() - t


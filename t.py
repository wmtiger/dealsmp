#!/usr/bin/env python
# -*- coning: utf-8 -*-
########################
#File Name:t.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-29 20:17:58
########################

import zbar
from PIL import Image

def deleteDuplicate(data):
    news_ids = []
    dataLen = len(data)
    for i in range(0, dataLen):
        if data[i] not in news_ids:
            news_ids.append(data[i])
    #print news_ids
    return news_ids

def readQR(box, sc, im, name):
    lfim = im.crop(box)
    lfim.save(name+"im.jpg")
    iw,ih = lfim.size
    lfraw = lfim.tostring()
    lfzim = zbar.Image(iw,ih,'Y800',lfraw)
    sc.scan(lfzim)
    data = []
    for sb in lfzim:
        data.append(sb.data)
    del(lfzim)
    return deleteDuplicate(data)

def scanLeft(sc, im, type):
    w,h = im.size
    if type == 0:
        box = (0,0,w/2,h)
    elif type == 1:
        box = (0,0,w/5*2,h)
    return readQR(box, sc, im, 'left')

def scanMiddle(sc, im, type):
    w,h = im.size
    if type == 1:
        box = (w/3,0,w/3*2,h)
    return readQR(box, sc, im, 'middle')

def scanRight(sc, im, type):
    w,h = im.size
    if type == 0:
        box = (w/2,0,w,h)
    elif type == 1:
        box = (w/5*3,0,w,h)
    return readQR(box, sc, im, 'right')

def scanImg(type, url = 'test.jpg'):
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with Image.open(url) as im:
        data=[]
        if type == 0:
            data.append(scanLeft(sc, im, type)[0])
            data.append(scanRight(sc, im, type)[0])
        elif type == 1:
            data.append(scanLeft(sc, im, type)[0])
            data.append(scanMiddle(sc, im, type)[0])
            data.append(scanRight(sc, im, type)[0])
        return data

if __name__ == '__main__':
    print scanImg(0)

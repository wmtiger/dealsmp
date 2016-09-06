#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:zt.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-07 12:59:28
########################

import picamera
import time
import io
import zbar
from PIL import Image

def get_qr2():
    s = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with picamera.PiCamera() as c:
        data = []
        c.resolution(640, 480)
        c.start_preview()
        time.sleep(0.1)
        while 1:
           if len(data) >= 2:
                break
            c.capture(s, format='jpeg')
            s.seek(0)
            pim = Image.open(s).convert('L')
            w, h = pim.size
            raw = pim.tostring()
            zim = zbar.Image(w, h, 'Y800', raw)
            sc.scan(zim) 
            for sb in zim:
                data.append(sb.data)
            del(zim)
        return data

def getQR():
    stream = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with picamera.PiCamera() as c:
#		c.resolution = (640, 480)
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
        return data

if __name__ == '__main__':
	data = get_qr2()
"""	
	while 1:
		if len(data) >= 2:
			break
		data = getQR()
	print data
"""
#	with picamera.PiCamera() as c2:
#		c2.start_preview()
#		time.sleep(0.2)
#		c2.capture('card.jpg')

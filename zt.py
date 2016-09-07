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

def getQR():
    stream = io.BytesIO()
    sc = zbar.ImageScanner()
    sc.parse_config("enable")
    with picamera.PiCamera() as c:
        c.start_preview()
        time.sleep(0.5)
        c.capture(stream, format='jpeg')
        stream.seek(0)
        pim = Image.open(stream).convert('L')
        w, h = pim.size
        raw = pim.tostring()
        zim = zbar.Image(w,h,'Y800', raw)
        sc.scan(zim)
        data = ''
        for sb in zim:
            data += sb.data
        del(zim)
        return data

if __name__ == '__main__':
        print getQR()

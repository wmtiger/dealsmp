#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:cmd_sendCard2.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-    09-07 10:46:06
########################

import cmdhandler
import picamera
from PIL import Image

def dealCard(s, re):
    print 'deal card'
    if re[0] == 0:
        # hands
        print 'hands'
        arr = getCardInfo(re[0])
    elif re[0] == 1:
        # flop
        print 'flop'
    elif re[0] == 2:
        # turn
        print 'turn'
    elif re[3] == 3:
        # river
        print 'river'
    else:
        print 'err'
        # err
    cmdhandler.sendMsg(s, 1002, arr)

def photoing():
    print 'is photo'

def analyzeQrcode():
    print 'analyze qrcode'

def getCardInfo(cardtype):
    print 'get card info '
    return [cardtype, 'ks,kc']

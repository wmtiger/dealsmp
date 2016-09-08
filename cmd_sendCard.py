#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:cmd_sendCard.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-    09-07 10:46:06
########################

import cmdhandler
import zbarreader
import conf

def dealCard(s, re):
    print 'deal card'
    if re[1] == 0:
        # hands
        print 'hands'
        arr = zbarreader.getHandQR()
    elif re[1] == 1:
        # flop
        print 'flop'
        arr = zbarreader.getFlopQR()
    elif re[1] == 2:
        # turn
        print 'turn'
        arr = zbarreader.getTurnQR()
    elif re[1] == 3:
        # river
        print 'river'
        arr = zbarreader.getRiverQR()
    else:
        print 'err'
        # err
        arr = []
    cardinfo = ''.join(arr)
    print cardinfo
    cmdhandler.sendMsg(s, 1002, [conf.position, re[1], cardinfo])

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
    if re[0] == 0:
        # hands
        print 'hands'
        arr = zbarreader.getHandQR()
        if len(arr)<2:
            print 'hands card len < 2'
            cmdhandler.sendMsg(s, 1003, [0])
            return
    elif re[0] == 1:
        # flop
        print 'flop'
        arr = zbarreader.getFlopQR()
        if len(arr)<3:
            print 'flop card len < 3'
            cmdhandler.sendMsg(s, 1003, [0])
            return
    elif re[0] == 2:
        # turn
        print 'turn'
        arr = zbarreader.getTurnQR()
        if len(arr)<4:
            print 'turn card len < 4'
            cmdhandler.sendMsg(s, 1003, [0])
            return
    elif re[0] == 3:
        # river
        print 'river'
        arr = zbarreader.getRiverQR()
        if len(arr)<5:
            print 'river card len < 5'
            cmdhandler.sendMsg(s, 1003, [0])
            return
    else:
        print 'err'
        # err
        arr = []
        cmdhandler.sendMsg(s, 1003, [0])
        return
    cardinfo = ','.join(arr)
    print cardinfo
    cmdhandler.sendMsg(s, 1002, [conf.position, re[0], cardinfo])

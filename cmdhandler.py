#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################
#File Name:cmdhandler.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-07 10:43:33
########################

import struct

cmdfmt = {
    # send to server cmd
    1001 : ['hs', ''],      # login 
    1002 : ['hhs', ''],      # send card [0]h is position, [1]h is step[0,1,2,3].
    1003 : ['h', ''],      # send card err.
    
    # get from server cmd
    2001 : ['h', 'loginHandler'],               # login result
    2002 : ['h', 'sendCardHandler'],            # send card result
    2003 : ['s', 'welcomeHandler'],             # welcome result
    2004 : ['h', 'startDealCardHandler'],       # start deal, need send card info to server. h=0(hands), h=1(flop), h=2(turn), h=3(river).
    2010 : ['h', 'killKeepHandle'],             # need kill keep shell

}

def pack(cmdId, data):
#   print cmdId, data
    global cmdfmt
    if cmdId not in cmdfmt:
        print cmdId, 'not in cmdfmt'
        return ''
        
    fmtStr = cmdfmt[cmdId][0]
#   print fmtStr
    fmtStrRes = []
    idx = 0
    fixString = {}
    for k in fmtStr:
        # count str length
        if k == 's':
            _strLen = len(data[idx])
            fixString[idx] = _strLen
            fmtStrRes.append(str(_strLen) + 's')
        else:
            fmtStrRes.append(k)
        idx += 1
        
    fmtStr2 = ''.join(fmtStrRes)
    fmtlen = len(fmtStr2)
    fmt = '<' + str(fmtlen) + 's'  + fmtStr2
    fmtsize = struct.calcsize(fmtStr2)
    data.insert(0, fmtStr2)
    body = struct.pack(fmt, *data)
    bodylen = len(body)
#   print body
    head = struct.pack('<ihh',bodylen,cmdId,fmtlen)
    return head + body

if __name__ == '__main__':
    print 'test'

#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:cmdhandler.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-    09-07 10:43:33
########################

import struct
import cmd_sendCard
import conf
import globalvar

cmdfmt = {
    # send to server cmd
    1001 : ['hs', ''],      # login 
    1002 : ['hhs', ''],      # send card [0]h is position, [1]h is step[0,1,2,3].
    1003 : ['h', ''],      # send card err.
    1010 : ['h', ''],      # send heart beat.
    
    # get from server cmd
    2001 : ['h', 'loginHandler'],               # login result
    2002 : ['h', 'sendCardHandler'],            # send card result
    2003 : ['s', 'welcomeHandler'],             # welcome result
    2004 : ['h', 'startDealCardHandler'],       # start deal, need send card info to server. h=0(hands), h=1(flop), h=2(turn), h=3(river).
    2010 : ['h', 'heartBeatHandler'],             # heart beat result

    3001 : ['2ishhhs', 'testHandler'],          # test
    3003 : ['iis', 'imgtestHandler'],           # test
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
        
#   print fmtStrRes
    fmtStr2 = ''.join(fmtStrRes)
    fmtlen = len(fmtStr2)
    fmt = '<' + str(fmtlen) + 's'  + fmtStr2
    fmtsize = struct.calcsize(fmtStr2)
#   print fmt, fmtsize, fmtStr2, fmtlen
    data.insert(0, fmtStr2)
    body = struct.pack(fmt, *data)
    bodylen = len(body)
#   print body
    head = struct.pack('<ihh',bodylen,cmdId,fmtlen)
    return head + body

def sendMsg(s, cmdId, params):
    msg = pack(cmdId, params)
    #print 'sendMsg', msg
    s.sendall(msg)

def loginHandler(s, re):
    #arr = cmd_login.getData(re)
    #sendMsg(s, 3003, arr)
    if re[0] == 0:
        print 'login faild'
    else:
        print 'login success'

def sendCardHandler(s, re):
    print 'send card'
    #print re
    #cmd_sendCard.getData(re)
    #sendMsg(s, 2002, arr)

def startDealCardHandler(s, re):
    print 'start deal'
    cmd_sendCard.dealCard(s, re)

def testHandler(s, re):
    print re

def welcomeHandler(s, re):
    print 'welcomeHandler: send login cmd to server'
    sendMsg(s, 1001, [conf.position,conf.name])

def imgtestHandler(s, re):
    print ''

def heartBeatHandler(s, re):
    print 'get server heart back'
    globalvar.needReconnect = 0

if __name__ == '__main__':
    print heartBeatHandler('s', [1])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################
#File Name:dealerclient.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-26 20:31:18
########################

import socket
import asyncore
import threading
import struct
import cmdhandler
import conf
import zbarreader
import os

class DealerClient(asyncore.dispatcher):

    buf = ''
    sendcmd = 0

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = bytes()

    def handle_connect(self):
        print 'connect'

    def handle_close(self):
        print 'close'
        self.close()

    def handle_read(self):
        BUFSIZE = 4096
        HEADSIZE = 8    # len:4; cmd:2; fmtlen:2
        databuf = ''
        temp = self.recv(BUFSIZE)
        if temp:
            databuf += temp
            while 1:
                if len(databuf) < HEADSIZE:
                    break
                headpack = struct.unpack('<ihh', databuf[:HEADSIZE])
                bodysize = headpack[0]
                cmdId = headpack[1]
                fmtsize = headpack[2]
                if len(databuf) < HEADSIZE + bodysize:
                    break
                fmt = databuf[HEADSIZE:HEADSIZE+fmtsize]
                body = databuf[HEADSIZE+fmtsize:HEADSIZE+bodysize]
                bodypack = struct.unpack('<'+fmt,body)
                #print 'bp',bodypack
                self.callCmdHandler(cmdId, bodypack)
                databuf = databuf[HEADSIZE+bodysize:]

    def callCmdHandler(self, cmd, params):
        print cmd, params
        if (cmd not in cmdhandler.cmdfmt):
            print cmd, 'not in cmdhander.cmdfmt'
            return 0
        funname = cmdhandler.cmdfmt[cmd][1]
        if (funname):
            fun = getattr(self, funname)
            if (callable(fun)):
                fun(params)
                self.sendcmd = cmd
            else:
                print 'fun not defined'
        else:
            print 'callback name is undefined'

    def writable(self):
        return len(self.buf) > 0 and self.sendcmd > 0

    def handle_write(self):
        print 'handle write', len(self.buf)
        sent = self.send(self.buf)
        self.sendcmd = 0
        self.buf = ''

    def startDealCardHandler(self, re):
        print 'start scan card and will send card'
        cardtype = ('hands', 'flop', 'turn', 'river')
        isErr = 0
        print 'start scan', cardtype[re[0]],'card'
        if re[0] == 0:
            # hands
            arr = zbarreader.getHandQR()
            if len(arr)<2:
                print 'hands card len < 2'
                isErr = 1
        elif re[0] == 1:
            # flop
            arr = zbarreader.getFlopQR()
            if len(arr)<3:
                print 'flop card len < 3'
                isErr = 1
        elif re[0] == 2:
            # turn
            arr = zbarreader.getTurnQR()
            if len(arr)<4:
                print 'turn card len < 4'
                isErr = 1
        elif re[0] == 3:
            # river
            arr = zbarreader.getRiverQR()
            if len(arr)<5:
                print 'river card len < 5'
                isErr = 1
        else:
            print 'err'
            # err
            isErr = 1
        if isErr == 1:
            self.buf = cmdhandler.pack(1003, [re[0]])
            return
        cardinfo = ','.join(arr)
        print cardinfo
        self.buf = cmdhandler.pack(1002, [conf.position, re[0], cardinfo])

    def sendCardHandler(self, re):
        if re[0] == 1:
            print 'send card ok'
        else:
            print 'send card faild'

    def welcomeHandler(self, re):
        self.buf = cmdhandler.pack(1001, [conf.position,conf.name+str(conf.position)])

    def loginHandler(self, re):
        if re[0] == 0:
            print 'login faild'
        else:
            print 'login success'

    def killKeepHandle(self, re):
        val = os.system("sh /home/pi/work/dealsmp/killkeep.sh")
        print 'kill state =', val

if __name__ == "__main__":
    print conf.severhost, conf.severport
    dealer = DealerClient(conf.severhost[0], conf.severport[0])
    asyncore.loop()

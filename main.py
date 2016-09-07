#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:main.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-    09-07 10:49:35
########################

import sys
import socket
import cmdhandler
import struct

def main(host, port):
    print 'mian start', host, port
    databuf = bytes()
    BUFSIZE = 4096
    HEADSIZE = 8    # len: 4, cmd: 2, fmtlen: 2

    s = socket.socket()
    connre = s.connect_ex((host,port))
    while 1:
        if connre == 0:
            break
        else:
            connre = s.connect_ex((host, port))
    
    #print 'Usage: cmd, [p1,...]'
    while 1:
    #   cmdandparams = raw_input('input cmd and params:')
    #   print cmdandparams
        temp = s.recv(BUFSIZE)
        if temp:
            databuf += temp
            while 1:
                if len(databuf) < HEADSIZE:
                    break
                headpack = struct.unpack('<ihh', databuf[:HEADSIZE])
#               print 'headpack:', headpack
                bodysize = headpack[0]
                cmdId = headpack[1]
                fmtsize = headpack[2]
                if len(databuf) < HEADSIZE + bodysize:
                    break
                fmt = databuf[HEADSIZE:HEADSIZE+fmtsize]
#               print 'fmt:',fmt
                body = databuf[HEADSIZE+fmtsize:HEADSIZE+bodysize]
                bodypack = struct.unpack('<'+fmt,body)
#               print 'bodypack',bodypack
                cmdHandler(s, cmdId, bodypack)
                databuf = databuf[HEADSIZE+bodysize:]

def cmdHandler(s, cmd, params):
#   print cmd, params
    if (cmd not in cmdhandler.cmdfmt):
        print cmd, 'not in cmdhander.cmdfmt'
        return 0
    funname = cmdhandler.cmdfmt[cmd][1]
#   print funname
    if (funname):
        fun = getattr(cmdhandler, funname)
        if (callable(fun)):
            fun(s, params)
        else:
            print 'fun not defined'
    else:
        print 'callback name is undefined'

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print 'usage: python',sys.argv[0], 'host port'
        host = '10.224.32.47'
        #host = '192.168.2.116'
        port = 9986
        main(host, port)
    else:
    #   sys.exit()
        main(sys.argv[1], int(sys.argv[2]))

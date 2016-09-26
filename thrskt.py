#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################
#File Name:thrskt.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-26 20:31:18
########################

import socket
import asyncore
import threading
import struct
import cmdhandler

class DealerClient(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = bytes()

    def handle_connect(self):
        print 'connect'

    def handle_close(self):
        print 'close', self.getpeername()
        self.close()

    def readabel(self):
        return True

    def handle_read(self):
        BUFSIZE = 4096
        HEADSIZE = 8    # len:4; cmd:2; fmtlen:2
        databuf = ''
        temp = self.recv(BUFSIZE)
        print 'a',temp
        if temp:
            databuf += temp
            print 'buf',databuf
            while 1:
                print 'len',len(databuf)
                if len(databuf) < HEADSIZE:
                    break
                headpack = struct.unpack('<ihh', databuf[:HEADSIZE])
                print 'pack',headpack
                bodysize = headpack[0]
                cmdId = headpack[1]
                fmtsize = headpack[2]
                print 'chk',len(databuf), HEADSIZE+bodysize
                if len(databuf) < HEADSIZE + bodysize:
                    break
                print 'here'
                fmt = databuf[HEADSIZE:HEADSIZE+fmtsize]
                print 'fmt',fmt
                body = databuf[HEADSIZE+fmtsize:HEADSIZE+bodysize]
                print 'by',body
                bodypack = struct.unpack('<'+fmt,body)
                print 'bp',bodypack
#                self.callCmdHandler(s, cmdId, bodypack)
                databuf = databuf[HEADSIZE+bodysize:]

    def callCmdHandler(s, cmd, params):
        if (cmd not in cmdhandler.cmdfmt):
            print cmd, 'not in cmdhander.cmdfmt'
            return 0
        funname = cmdhandler.cmdfmt[cmd][1]
        if (funname):
            fun = getattr(cmdhandler, funname)
            if (callable(fun)):
                fun(s, params)
            else:
                print 'fun not defined'
        else:
            print 'callback name is undefined'

    def writable(self):
#        print 'writable'
        return False

    def handle_write(self):
        print 'write'
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

class send_server_thread(threading.Thread):
    def __init__(self, host, port):
        self.client = DealerClient(host, port)
        threading.Thread.__init__(self)

    def run(self):
        try:
            asyncore.loop()
        except:
            pass

class input_thread(threading.Thread):
    def __init__(self, client_thread):
        self.client_thread = client_thread
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            send_data = raw_input()
            self.client_thread.client.SendData = send_data
            self.client_thread.client.handle_write()


if __name__ == "__main__":
#    dealer = DealerClient('192.168.2.112', 9986)
#    asyncore.loop()
    client_thread = send_server_thread('192.168.2.112', 9986)
    client_thread.start()
    input_thread(client_thread).start()

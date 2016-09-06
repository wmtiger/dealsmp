#!/usr/bin/env python
# -*- coding: utf-8 -*-
#auther: wsm
#version: 1.0

import struct
import base64
from PIL import Image

cmdfmt = {
	# send to server cmd
	1001 : ['ss', ''],		# login 
	1002 : ['s', ''],			# send card
	
	# get from server cmd
	2001 : ['h', 'loginHandler'],				# login result
	2002 : ['h', 'sendCardHandler'],			# send card result
	2003 : ['s', 'welcomeHandler'],				# welcome result

	3001 : ['2ishhhs', 'testHandler'],			# test
	3003 : ['iis', 'imgtestHandler'],			# test
}

def pack(cmdId, data):
#	print cmdId, data
	global cmdfmt
	if cmdId not in cmdfmt:
		print cmdId, 'not in cmdfmt'
		return ''
		
	fmtStr = cmdfmt[cmdId][0]
#	print fmtStr
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
		
#	print fmtStrRes
	fmtStr2 = ''.join(fmtStrRes)
	fmtlen = len(fmtStr2)
	fmt = '<' + str(fmtlen) + 's'  + fmtStr2
	fmtsize = struct.calcsize(fmtStr2)
#	print fmt, fmtsize, fmtStr2, fmtlen
	data.insert(0, fmtStr2)
	body = struct.pack(fmt, *data)
	bodylen = len(body)
#	print body
	head = struct.pack('<ihh',bodylen,cmdId,fmtlen)
	return head + body

def sendMsg(s, cmdId, params):
	msg = pack(cmdId, params)
	#print 'sendMsg', msg
	s.sendall(msg)

def loginHandler(s, re):
#	print re
	print 'ready to use camera'
	im = Image.open('img.jpg')
	w,h = im.size
	print w, h
	f = open('img.jpg', 'rb')
	ls_f = base64.b64encode(f.read())
	f.close()
	sendMsg(s, 3003, [w,h,ls_f])

def sendCardHandler(s, re):
	print re

def testHandler(s, re):
	print re

def welcomeHandler(s, re):
	print 'welcomeHandler'
	sendMsg(s, 1001, ['smp4','wsm'])

def imgtestHandler(s, re):
	#print 're len:',len(re[2])
	fh = open('test.jpg', 'wb')
	str64 = re[2]
#	print str64
	data = bytes()
	data+=base64.b64decode(str64)
	print len(data)
#	fh.write(base64.b64decode(str64))
	fh.close()

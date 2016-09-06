#!/usr/bin/env python
# -*- conding: utf-8 -*-
########################
#File Name:cmd_sendCard.py
#Author:WmTiger
#Mail:bfstiger@gmail.com
#Created Time:2016-09-06 23:07:52
########################

import cmdhandler
import picamera
from PIL import Image

def dealCard(s, re):
	print 'deal card'
	if re[0] == 0:
		# hands
		
	elif re[0] == 1:
		# flop

	elif re[0] == 2:
		# turn

	elif re[3] == 3:
		# river

	else:
		# err
	cmdhandler.sendMsg(s, cmdId, arr)

def photoing():
	print 'is photo'

def analyzeQrcode():
	print 'analyze qrcode'

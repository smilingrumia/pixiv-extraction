#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os
import sys
import time
import re
from subprocess import Popen, call, PIPE
from tkinter import Tk

# Move to script directory
os.chdir( os.path.dirname(os.path.abspath(__file__)) )

SAVE_IMAGES_DIR = 'save_images/'
SAVE_UGOIRA_DIR = 'save_ugoira/'
TEMP_DIR = 'tmp/'
DEVNULL = open(os.devnull, 'w')

'''
 Save format

 0: title.jpg
    title(artId).jpg
 1: artId.jp
'''
SAVE_FORMAT = 0


# includes
exec(compile(open('support.py').read(),filename='support.py', mode='exec'))
exec(compile(open('httpHeader.py').read(),filename='httpHeader.py', mode='exec'))
exec(compile(open('pixiv_extraction.py').read(),filename='pixiv_extraction.py', mode='exec'))


# Main

urls = []


# from Clipboard
if(len(sys.argv) == 2):
  if(sys.argv[1] == '-c'):
    urls = getUrlsFromClipboard()
# from Arg
if(len(sys.argv) > 1):
  if(sys.argv[1] != '-c'):
    urls = sys.argv[1:]
# None Arg
else:
  print('[Usage]')
  print('./exctaction.sh url1 url2 ...')
  print('./exctaction.sh -c')
  sys.exit(0)


# DL loop
cnt = 1
for url in urls:
  print( str(cnt) + '/' + str(len(urls)))
  cnt += 1
  if( pixiv_extraction(url) == False):
    print('Failed: ' + url)
    sys.exit(1)

if( cnt > 1):
  print('Completed!')


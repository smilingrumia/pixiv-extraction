#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import shutil
import gzip
import brotli
from subprocess import Popen, call, PIPE
from tkinter import Tk
from shutil import copyfile
from os import listdir
from os.path import isfile, join

# Move to script directory
os.chdir( os.path.dirname(os.path.abspath(__file__)) )

SAVE_IMAGES_DIR = 'save_images/'
SAVE_UGOIRA_DIR = 'save_ugoira/'
TEMP_DIR = 'tmp/'
DEVNULL = open(os.devnull, 'w')
VERBOUSE = 0

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
exec(compile(open('pixiv.py').read(),filename='pixiv.py', mode='exec'))


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
  print('[Version]')
  print('  v0.7.5')
  print('')
  print('[Usage]')
  print('  ./exctaction.sh url1 url2 ...')
  print('  ./exctaction.sh -c')
  print('')
  sys.exit(0)


# Art DL loop
cnt = 1
for url in urls:
  if(VERBOUSE == 1):
    print( str(cnt) + '/' + str(len(urls)))
  if( pixiv_extraction(url, str(cnt), str(len(urls))) == False):
    print('Failed: ' + url)
    sys.exit(1)
  cnt += 1

if( cnt > 1):
  print('Complet!')
  sys.exit(0)


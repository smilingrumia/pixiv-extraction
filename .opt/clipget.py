#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import shutil
from tkinter import Tk
from os import listdir
from os.path import isfile, join

# Move to script directory
os.chdir( os.path.dirname(os.path.abspath(__file__)) )

def getUrlsFromClipboard():
  r = Tk()
  r.withdraw()

  # Ignore the current clipboard data
  try:
    urls = [r.clipboard_get()]
  except:
    # is empty
    urls = ['']

  print('Listening on clipboard...')
  try:
    while True:
      try:
        s = r.clipboard_get()

        # new clipboard text?
        if( urls[len(urls) - 1] != s):
          urls.append(s)
          print(s)

      except:
        None
      time.sleep(0.1)
  except:
    print()

  return urls[1:]



# Main
urls = []

# from Clipboard
urls = getUrlsFromClipboard()
f = open("dllist", 'w')
for url in urls:
  print( url, file=f)
f.close()

print()
print('Dump to dllist')
sys.exit(0)


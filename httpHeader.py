#!/usr/bin/python3

# -*- coding: utf-8 -*-


# Pixiv
def getHttpHeader_pixiv_artpage():
  return getHttpHeader('httpHeader/pixiv_artpage')

def getHttpHeader_pixiv_artlist():
  return getHttpHeader('httpHeader/pixiv_artlist')

def getHttpHeader_pixiv_art():
  return getHttpHeader('httpHeader/pixiv_art')


def getHttpHeader(f):
  rHeader = ''
  try:
    fp = open(f, 'r')
    line = fp.readline()
    while(line):
      lineString = line.strip()
      if(lineString == ''):
        break
      else:
        rHeader +=  lineString + "\r\n"
        line = fp.readline()
    return rHeader + "\r\n"
  except:
    return ''


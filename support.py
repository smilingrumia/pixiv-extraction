
def prepareHttpHeaderWithReferer(header, referer):
  try:
    hlen = len(re.search('Referer: ([a-z,A-Z,0-9,\.,\/,\-,\_,\:]*)', header).group(0) )
    start = header.find('Referer: ')
    return header[0:start] + 'Referer: '+ referer + header[start+hlen:]
  except:
    print('Error: prepareHttpHeaderWithReferer')
    return False


def prepareToCurl(url, header):
  r = ['curl', url]

  try:
    for l in header.splitlines():
        r.append('-H')
        r.append(l)
    return r
  except:
    return 'error'


def getHttp(url, header):
  global DEVNULL

  req = prepareToCurl(url, header)
  #print(req)
  #time.sleep(3)

  p = Popen(req, stdout=PIPE, stderr=DEVNULL)
  p.wait()
  if( p.returncode == 0):
    print('Ok: ' + url)
    return p.communicate()[0]
  else:
    print('Failed: ' + url)
    return False


def getAndSaveHttp(url, header, save):
  global DEVNULL

  req = prepareToCurl(url, header)
  #print(req)
  #time.sleep(3)

  p = Popen(req, stdout=open(save,'wb'), stderr=DEVNULL)
  p.wait()
  if( p.returncode == 0):
    print('Ok: ' + url)
    return True
  else:
    print('Failed: ' + url)
    return False


def unzipAndSave(src, dst):
  global DEVNULL

  p = Popen(['7z', '-y', 'x', src, '-o' + dst], stdout=DEVNULL, stderr=DEVNULL)
  p.wait()
  if( p.returncode == 0):
    return True
  else:
    return False


def convertUgoiraToMp4(src, frate, dst):
  global DEVNULL

  ffmpegcmd = ['ffmpeg', '-y', '-framerate', str(frate), '-i', src, '-vcodec', 'copy', dst]
  p = Popen(ffmpegcmd, stderr=DEVNULL)
  p.wait()
  if( p.returncode == 0):
    return True
  else:
    return False


def getUrlsFromClipboard():
  r = Tk()
  r.withdraw()

  # urllist, Ignoring the current clipboard data
  urls = [r.clipboard_get()]

  print('------------ Listening Clipboard ---------------')
  try:
    while True:
      try:
        s = r.clipboard_get()
        if( urls[len(urls) - 1] != s):
          urls.append(s)
          print(s)
      except:
        None
      time.sleep(0.3)
  except:
    print()
  
  print('---------- The follow will be downloaded -----------')
  for url in urls[1:]:
    print(url)
  
  print('\nIs Ok?(y/n)')
  if( input() == 'y'):
    return urls[1:]
  else:
    return []


def saveArtInformation(info_file, art_url, img_length, art_title, art_artist, art_comment):
  def printToFile(s, f):
    print(s, file=f)

  f = open(info_file,'w')
  printToFile('[Url]', f)
  f.close()

  f = open(info_file,'a')
  printToFile(art_url, f)
  printToFile('', f)
  if( img_length > 1):
    printToFile('[Img length]', f)
    printToFile(str(img_length), f)
    printToFile('', f)
  printToFile('[Title]', f)
  printToFile(art_title, f)
  printToFile('', f)
  printToFile('[Artist]', f)
  printToFile(art_artist, f)
  printToFile('', f)
  printToFile('[Comment]', f)
  printToFile(art_comment, f)
  printToFile('', f)
  printToFile('', f)
  f.close()


def excludeCharacterFromArtInfo(info):
  info = info.replace('&amp','&')
  info = info.replace(';','')
  info = info.replace('\'','')
  info = info.replace('/','')
  info = info.replace('.','')
  return info


def prepareOutputFileName(output_dir, art_title, art_id, numTag, ext):
  at = excludeCharacterFromArtInfo(art_title)
  ai = excludeCharacterFromArtInfo(art_id)
  e = excludeCharacterFromArtInfo(ext)

  try:
    if(numTag != ''):
      f = open(output_dir + at + numTag + '.' + ext)
    else:
      f = open(output_dir + at + '.' + ext)
    f.close()
    return output_dir + at + '(' + ai + ')' + numTag + '.' + e
  except:
    if(numTag != ''):
      return output_dir + at + numTag + '.' + e
    else:
      return output_dir + at + '.' + e


def calculateFrameRate(ugoira_meta):
  try:
  # frame-rate calculation
    collected_delays = []
    collected_delays_cnt = []
    cnt = 0
    for delay in re.findall('delay\"\:([0-9]{1,4})\}',ugoira_meta.decode()):
      d = int(delay)

      # Too much frame?
      if( cnt > 10000 ):
        print('Too much frame')
        return False
      cnt += 1
    
      # Strange delay?
      if( d <= 0 or d > 3000 ):
        print('Strange delay')
        return False
    
      # is first-seeing delay?
      is_firstSeeing_delay = True
      for i in range(0, len(collected_delays)):
        if(collected_delays[i] == d):
          is_firstSeeing_delay = False
          collected_delays_cnt[i] = collected_delays_cnt[i] + 1
          break
      if(is_firstSeeing_delay):
        collected_delays.append(d)
        collected_delays_cnt.append(1)
    
    #print(collected_delays)
    #print(collected_delays_cnt)
  
    # Constant delay
    if( len(collected_delays) == 1 ):
      return int(1000 / collected_delays[0])

    # un-Constant delay ()
    else:
      print()
      print('WARNING')
      print('Original frame rate is un-constant')
      print('We will use the \'most used delay\' to calculate the frame-rate')
      print('This may have some impact on the art frame-rate.')
      print()
      major = 0
      delayToUse = 40
      for i in range(0, len(collected_delays_cnt)):
        if( collected_delays_cnt[i] > major):
          major = collected_delays_cnt[i]
          delayToUse = collected_delays[i]
      #print('delayToUse: ' + str(delayToUse))
      return int(1000 / delayToUse)
  except:
    return False



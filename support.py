
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


def decompressHtml(d):
  # gzip
  try:
    return gzip.decompress(d)
  except:
    # brotli
    try:
      return brotli.decompress(d)
    # else
    except:
      return d

def getHttp(url, header):
  global DEVNULL

  c = prepareToCurl(url, header)
  #print(c)
  #time.sleep(3)

  p = Popen(c, stdout=PIPE, stderr=DEVNULL)
  p.wait()
  if( p.returncode == 0):
    print('Ok: ' + url)
    return decompressHtml(p.communicate()[0])
  else:
    print('Failed: ' + url)
    return False


def getAndSaveHttp(url, header, save):
  global DEVNULL

  c = prepareToCurl(url, header)
  #print(c)
  #time.sleep(3)

  f = open(save, 'wb')
  p = Popen(c, stdout=f, stderr=DEVNULL)
  p.wait()
  f.close()
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


def convertUgoiraToMp4(isCfr, art_id, frate, frameLen, ext, output):
  global TEMP_DIR
  global DEVNULL

  # for some reason, ffmpeg skip the first frame, so wi will make 2 first frame
  for i in reversed(range(0, frameLen)):
    src = TEMP_DIR + art_id + '/{:06d}.'.format(i) + ext
    dst = TEMP_DIR + art_id + '/{:06d}.'.format(i+1) + ext
    copyfile(src, dst)


  # CFR(constant frame rate)
  if(isCfr == True):
    c = ['ffmpeg', '-y', '-framerate', str(frate), '-i', TEMP_DIR + art_id + '/%06d.'+ext, '-vcodec', 'copy', output]
    p = Popen(c, stderr=DEVNULL)
    p.wait()
    if( p.returncode == 0):
      return True
    else:
      return False

  # VFR(variable frame rate)
  else:
    # make timecode
    f=open(TEMP_DIR + art_id + '/timecode.txt', 'w')
    print( '# timecode format v2',file=f)
    print( '',file=f)
    print( '0',file=f)
    print( '1',file=f)
    time=1
    for t in frate:
      time += t
      print( str(time),file=f)
    f.close()

    # images -> mp4
    c = ['ffmpeg', '-y', '-i', TEMP_DIR + art_id + '/%06d.'+ext, '-vcodec', 'copy', TEMP_DIR + art_id + '/ugoira.mp4']
    p = Popen(c, stderr=DEVNULL)
    p.wait()
    if( p.returncode != 0):
      return False

    # make mp4 as vfr
    #  is better to use -x ? 
    c = ['./mp4fpsmod', '-o', output, '-x', '-t', TEMP_DIR + art_id + '/timecode.txt', TEMP_DIR + art_id + '/ugoira.mp4']
    #c = ['./mp4fpsmod', '-o', output, '-t', TEMP_DIR + art_id + '/timecode.txt', TEMP_DIR + art_id + '/ugoira.mp4']
    p = Popen(c, stderr=DEVNULL)
    p.wait()
    if( p.returncode == 0):
      return True
    else:
      return False


def getUrlsFromClipboard():
  r = Tk()
  r.withdraw()

  # Ignore the current clipboard data
  try:
    urls = [r.clipboard_get()]
  except:
    # is empty
    urls = ['']

  print('------------ Listening on clipboard ---------------')
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
  
  print('---------- The follow will be download ------------')
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
  global SAVE_FORMAT

  at = excludeCharacterFromArtInfo(art_title)
  ai = excludeCharacterFromArtInfo(art_id)
  e = excludeCharacterFromArtInfo(ext)

  # title.jpg or title(id).jpg
  if (SAVE_FORMAT == 0):
    try:
      if(numTag != ''):
        f = open(output_dir + at + numTag + '.' + ext)
      else:
        f = open(output_dir + at + '.' + ext)
      f.close()
      # allready have title.jpg so return out/title(id).jpg
      return output_dir + at + '(' + ai + ')' + numTag + '.' + e

    # dont have title.jpg
    except:
      # return out/title_001.jpg
      if(numTag != ''):
        return output_dir + at + numTag + '.' + e
      # return out/title.jpg
      else:
        return output_dir + at + '.' + e

  # id.jpg
  elif (SAVE_FORMAT == 1):
    if(numTag != ''):
      return output_dir + ai + numTag + '.' + e
    else:
      return output_dir + ai + '.' + e


'''
  Return
    isOk True/False
    type 0=CFR 1=VFR
    frame-rate int=CFR,list=VFR
    frame-length int
'''
def calculateFrameRate(ugoira_meta):
  try:
    frames = []
    delays = []
    frame_delays = []
    cnt = 0

    # Frames
    for frame in re.findall('file\":\"([0-9]{1,6})\.',ugoira_meta.decode()):
      f = int(frame)

      # Strange frame?
      if( f < 0 or f > 999999 ):
        print('Strange frame')
        return (False, 0, 0, 0)
    
      frames.append(f)
      frame_delays.append(False)

    # Delays
    for delay in re.findall('delay\"\:([0-9]{1,4})\}',ugoira_meta.decode()):
      d = int(delay)

      # Too much frame?
      if( cnt > 10000 ):
        print('Too much frame')
        return (False, 0, 0, 0)
      cnt += 1

      delays.append(d)

    # Frame mismatch?
    if( len(frames) != len(delays) ):
      print('length of frames/delays mismatch')
      return (False, 0, 0, 0)

    # No frame?
    if( len(frames) <= 0 or len(delays) <= 0 ):
      print('length of frames/delays is less than 0?')
      return (False, 0, 0, 0)

    # Put delay on right place
    for i in range(0, len(frames)):
      if( frames[i] < 0 or frames[i] >= len(frames)):
        print('Strange frame number')
        return (False, 0, 0, 0)
      frame_delays[frames[i]] = delays[i]

    # Confirm
    for fd in frame_delays:
      if(fd == False):
        print('Strange frame_delays')
        return (False, 0, 0, 0)

    isVariableFrameRate = False
    prev_d = False
    for d in frame_delays:
      if( prev_d != False):
        if( prev_d != d):
          isVariableFrameRate = True
          break
      prev_d = d


    # CFR
    if( isVariableFrameRate == False ):
      return (True, 0, float(1000 / frame_delays[0]), len(frame_delays))

    # VFR
    else:
      print('info: This Ugoira is VFR')

      # Don't have mp4fpsmod to make VFR mp4?
      if(not os.path.exists('mp4fpsmod')):
        print('WARNING')
        print(' mp4fpsmod is not installed, without this we can\'t make Ugoira as VFR.')
        print(' Ugoira will be saved as CFR(Constant frame rate) with fps as the middle.')

        # Calculate the middle
        fcnt = len(frame_delays)
        fsum = 0
        for t in frame_delays:
          fsum += t
        return (True, 0, float(1000 / float(fsum / fcnt)), fcnt)

      # mp4fpsmod is installed 
      else:
        return (True, 1, frame_delays, len(frame_delays))
  except:
    return (False, '', '', 0)


def saveArtUgoiraMeta(dst, ugoira_meta):
  f = open(dst,'wb')
  f.write(ugoira_meta)
  f.close()


def cleanUgoiraZip(path):
  if isfile(path):
    os.remove(path)


def cleanUgoiraTempFile(path):
  for f in listdir(path):
    if isfile(join(path, f)):

      if( re.match('[0-9]{6}\.(jpg|png)', f)):
        continue

      elif( re.match('timecode.txt', f)):
        continue

      elif( re.match('ugoira\.mp4', f)):
        continue

      # Strange file contain..., we wont delete this dir
      else:
        return False

    # Strange dir contain..., we wont delete this dir
    else:
      return False

  shutil.rmtree(path)


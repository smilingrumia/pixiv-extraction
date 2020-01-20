#!/usr/bin/python3

# -*- coding: utf-8 -*-


# for Images DL
def pixiv_imagesExtraction(art_url, art_id, art_title, art_artist, art_comment, img_original_sample):

  global SAVE_IMAGES_DIR
  global SAVE_FORMAT

  # Extract img list
  artlist_url = 'https://www.pixiv.net/ajax/illust/' + art_id +'/pages'
  r = getHttp(artlist_url, prepareHttpHeaderWithReferer(getHttpHeader_pixivArtMeta(), art_url))
  if (r == False):
    return False

  # Image length
  img_length = len(re.findall('img-original',str(r)))
  if ( img_length <= 0 or img_length >= 500 ):
    print('img_length is strange')
    return False
  print(str(img_length)+' images')
  
  # Image extraction
  for i in range(0,img_length) :
    try:
      exp = re.search('\.(jpg|jpeg|png|gif)$', img_original_sample).group(1)
      first = img_original_sample.find('_p')
      img_url = img_original_sample[0:first+2] + str(i) + '.' + exp

      # Retry if fail
      r = False
      for j in range(1,3):
        if(SAVE_FORMAT == 0):
          save_path = prepareOutputFileName(SAVE_IMAGES_DIR, art_title, art_id, "_{:03d}".format(i + 1), exp)
        elif(SAVE_FORMAT == 1):
          save_path = SAVE_IMAGES_DIR + art_id + "_{:03d}".format(i + 1) + '.' + exp

        r = getAndSaveHttp(img_url, prepareHttpHeaderWithReferer(getHttpHeader_pixivArtContent(), art_url), save_path)
        if (r != False):
          break
        else:
          print("Retrying! ")
      if( r == False ):
        print('DL fail even retrying')
        return False
    except:
      return False
  
  # Save art information
  info_file = prepareOutputFileName(SAVE_IMAGES_DIR + 'info/', art_title, art_id, '', 'txt')
  saveArtInformation(info_file, art_url, img_length, art_title, art_artist, art_comment)

  print('Ok: ' + art_title)
  return True



# for Ugoira DL
def pixiv_ugoiraExtraction(art_url, art_id, art_title, art_artist, art_comment, img_original_sample):

  global SAVE_UGOIRA_DIR
  global TEMP_DIR

  # Extract ugoira meta-data
  try:
    artlist_url = 'https://www.pixiv.net/ajax/illust/'+ art_id + '/ugoira_meta'
    r = getHttp(artlist_url, prepareHttpHeaderWithReferer(getHttpHeader_pixivArtMeta(), art_url))
    if(r == False):
      return False

    # Save ugoira_meta
    ugoira_meta_file = prepareOutputFileName(SAVE_UGOIRA_DIR + 'info/', art_title, art_id, '', 'ugoira_meta')
    saveArtUgoiraMeta(ugoira_meta_file, r)

  except:
    print('Fail to Get ugoira_meta')
    return False

  # Get Ugoira URL: https:\/\/i.pximg.net\/img-zip-ugoira\/img\/<something>_ugoira1920x1080.zip
  # And
  # Convert to:     https://i.pximg.net/img-zip-ugoira/img/<something>_ugoira1920x1080.zip
  try:
    raw_ugoira_url = re.findall('originalSrc\"\:\"(https\:\\\/\\\/i.pximg.net[a-z,A-Z,0-9,\.,\/,\-,\_,\\\]*zip)',r.decode())[0]
    ugoira_url =''
    now =0
    for i in range(0,60):
      next = raw_ugoira_url[now:].find('\\')
      ugoira_url += raw_ugoira_url[now:now+next]
      now += next + 1
    ugoira_url += raw_ugoira_url[now:]
  except:
    print('Fail to Get Ugoira URL')
    return False

  # Frame-rate calculation
  frSum = calculateFrameRate(r)
  if(frSum[0] == False):
    print('Fail to calculateFrameRate')
    return False

  # DL ugoira.zip
  try:
    r = getAndSaveHttp(ugoira_url, prepareHttpHeaderWithReferer(getHttpHeader_pixivArtContent(), art_url), TEMP_DIR + art_id + ".zip")
    if (r == False):
      print('Fail to DL The Zip' + url)
      return False
  except:
    print('Fail to DL the zip')
    return False

  # ugoira dirs
  ugoira_zip = TEMP_DIR + art_id + ".zip"
  ugoira_dir = TEMP_DIR + art_id
  ugoira_out = prepareOutputFileName(SAVE_UGOIRA_DIR, art_title, art_id, '', 'mp4')

  # Unzip
  r = unzipAndSave(ugoira_zip, ugoira_dir)
  if ( r == False):
    print('Fail to unzip')
    return False
  os.remove(ugoira_zip)

  # ffmpgeg
  ext = ''
  # jpg
  try:
    f = open(ugoira_dir + '/000000.jpg', 'r')
    f.close()
    ext = 'jpg'
  # png
  except:
    try:
      f = open(ugoira_dir + '/000000.png', 'r')
      f.close()
      ext = 'png'
    except:
      print('Fail: Ugoira is not jpg or png?')
      return False

  # Is CFR
  if(frSum[1] == 0):
    r = convertUgoiraToMp4(True, art_id, frSum[2], frSum[3], ext, ugoira_out)
  # Is VFR
  elif(frSum[1] == 1):
    r = convertUgoiraToMp4(False, art_id, frSum[2], frSum[3], ext, ugoira_out)
  else:
    print('Fail: not CFR or VFR?')
    return False

  if ( r == False):
    print('Fail to ffmpeg')
    return False

  # Save art information
  info_file = prepareOutputFileName(SAVE_UGOIRA_DIR + 'info/', art_title, art_id, '', 'txt')
  saveArtInformation(info_file, art_url, 1, art_title, art_artist, art_comment)

  print('Ok: ' + art_title + '.mp4')
  return True



# Pixiv Main
def pixiv_extraction(art_url):

  # Validate Pixiv URL
  if(not re.search('^https\:\/\/www.pixiv.net([a-z,\/]{1,8})artworks/([0-9]{1,10})$',art_url)):
    print('Not pixiv\'s art url')
    return False

  # Extract art_id
  try:
    art_id = re.search('artworks\/([0-9]{1,10})',art_url).group(1)
  except:
    print("URL dont contain art_id?")
    return False


  # Get art page
  r = getHttp(art_url, getHttpHeader_pixivArtPage())
  if (r == False):
    return False


  # Art original-size img url sample
  try:
    i = re.search('jpg\"\,\"original\"\:\"(http\:\/\/|https\:\/\/)([a-z,A-Z,0-9,\.,\/,\-,\_]*)',str(r))
    img_original_sample = str(i.group(1) + i.group(2))
  except:
    print('img_original_sample is strange')
    return False

  # Art title
  try:
    i = r.find(b'illustTitle":"') + len('illustTitle":"')
    ii = r[i:].find(b'"')
    art_title = excludeCharacterFromArtInfo(r[i:i+ii].decode('utf-8'))
  except:
    print('art_title is strange')
    return False

  # Art artist
  try:
    i = r.find(b'userName":"') + len('userName":"')
    ii = r[i:].find(b'"')
    art_artist = excludeCharacterFromArtInfo(r[i:i+ii].decode('utf-8'))
  except:
    print('art_artist is strange')
    return False

  # Art comment
  try:
    i = r.find(b'illustComment":"') + len('illustComment":"')
    ii = r[i:].find(b'"')
    art_comment = excludeCharacterFromArtInfo(r[i:i+ii].decode('utf-8'))
  except:
    # Ignore comment if failed
    art_comment = ''


  # Images/Ugoira decision
  try:
    i = r.find(b'_ugoira0')
    ii = r[i:i+60].find(b'"authorId"')

    # Ugoira
    if( ii != -1):
      return pixiv_ugoiraExtraction(art_url, art_id, art_title, art_artist, art_comment, img_original_sample)
    # Images
    else:
      return pixiv_imagesExtraction(art_url, art_id, art_title, art_artist, art_comment, img_original_sample)
  except:
    print('Images/Ugoira failed')
    return False



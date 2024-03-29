
# pixiv-extraction
CLI tool to download pixiv image and ugoira [without loss of quality.](#detail-of-lossless)


OS: Linux,Windows10  
Version: 0.7.6  

**12/2023: usable**

# Overview
- [Install](#Install)
	- [Windows](#windows)
	- [Linux](#linux)
	- [Add cookies](#add-cookies)
	- [mpv](#install-mpv)
- [Run](#run)
- [Notes](#notes)
	- Detail of lossless
	- Play ugoira on smartphone?
	- Art filename
	- Clipboard pickup + yt-dlp
	- How to make lossless ugoira(for developer)
----------------------------

 
# Install

### Windows
see [README(Windows10)](https://github.com/smilingrumia/pixiv-extraction/blob/master/README(Windows10).md)

### Linux
```
git clone https://github.com/smilingrumia/pixiv-extraction   
sudo apt update
sudo apt install curl p7zip-full ffmpeg python3-tk python3-brotli
```

Open [mp4fpsmod](https://github.com/nu774/mp4fpsmod) -> Release -> DL the latest(here will be 0.26)
```
# some deps that need
sudo apt install autoconf libtool

tar xf mp4fpsmod-0.26.tar.gz
cd mp4fpsmod-0.26
./bootstrap.sh
./configure
make

# move compiled binary to pixiv-extraction/
mv ./mp4fpsmod <path>/pixiv-extraction/
```

## Add cookies
We need your cookie(login-credential) to get the art.  
I will explain how to get cookies and place in pixiv-extraction folder using firefox.  
  
**Step 1**  
Run firefox and login to Pixiv.  
Open an art, address bar will look like:  ```https://www.pixiv.net/en/artworks/12345678```  
  
F12(open devtool) -> Network tab -> F5/Refresh the Pixiv page  
A list in Network tab will be displayed.  
May be on the top,  
select: Domain(```www.pixiv.net```) File(12345678) Type(html)  
  
On the right window, goto Headers-> Request Headers  
Turn ON Raw headers  
Right Click -> select all -> Right Click -> copy  
  
Open pixiv-extraction/httpHeader/pixiv_artpage with text-editor and paste your header    
This Header must contain Cookie  
  
Save.  
  
**Step 2**  
Next in Network tab  
select one with: Type(json)  
And like Step 1, copy&pasete the header to pixiv-extraction/httpHeader/pixiv_artlist  
This Header must contain Cookie and x-user-id  
  
Save.  
  
Close devtool.  
  
**Step 3**  
Open some art(picture)  
Right click 1 image -> Open link in new window  
Address bar will look like: ```https://i.pximg.net/img-original/img/2016/01/02/03/04/05/12345678_p0.png```  
  
F12(open devtool) -> Network tab -> F5/Refresh the Pixiv page  
On Network tab, select: Domain(```i.pixiv.net```) File(12345678_p0.png)  
and copy&paste the header to pixiv-extraction/httpHeader/pixiv_art  

if contain follow, EXCLUDE THAT LINE!
```
If-Modified-Since: <something>
Range: <something>
If-Range: <something>
```

This Header DON’T contain Cookie or x-user-id  
  
Save.  


## install mpv
mpv shoud play ugoira(mjpeg) smoothly.    
install the latest mpv.  

**configure**  
edit mpv.conf  
Linux: nano ~/.config/mpv/mpv.conf  
```
loop
idle=yes
force-window

# volume more than 100% brakes sound quality
volume-max=100

# don't show notifications when change volume, seek ,etc
osd-level=0

# play on original size
video-unscaled=yes

# this may help on "viewing big ugoira -> press 'n' to go to next, but mpv still fixed big"
#no-border
```
Edit input.conf  
Linux: nano ~/.config/mpv/input.conf  
```
UP     add volume 5
DOWN   add volume -5
n      playlist-next    
p      playlist-prev
```

**mpv basic commands**  
```
 n          next video     (this works when Drug&Drop multiple .mp4 on mpv)
 p          previous video (this works when Drug&Drop multiple .mp4 on mpv)
 UP         volume up
 DOWN       volume down
 RIGHT      5sec next
 LEFT       5sec back
 Alt+RIGHT  right rotate
 Alt+LEFT   left rotate
 f          full screen
 q          quit
```

# Run  
**Normal mode**  
```./extraction.py URL1 URL2 ...```  
  
this will look like  
```./extraction.py https://www.pixiv.net/en/artworks/12345678 https://www.pixiv.net/en/artworks/23456789 ...```  
  
   
**Clipboard mode**  
```./extraction.py -c```  
  
On firefox Right Click -> L on the art thumbnail should copy the URL.  
copied URL shuld look like: ```https://www.pixiv.net/en/artworks/12345678```  
do this on all art that you want.  

Ctrl+C on the terminal, type y and Enter to start download.  
  
To see version, just Run ./extraction.py  

**Where is saved?**  
Images: save_images/  
Ugoira: save_ugoira/  
  
# Notes  

### Detail of lossless
  
**Images**  
Original image are downloaded.  
  
**Ugoira**  
Technically ugoira is sort of jpeg and frame-rate information.  
each one image, have X millisecond to wait, this mean that ugoira is VFR(variable frame rate)  

To be lossless as image-quality and frame-rate, pixiv-extraction save ugoira as VFR mjpeg(conventionally as .mp4)  
is not gif,apng,webm or lossy mp4.  

And can revert to original ugoira images with:  
```
ffmpeg -i ugoira.mp4 -vcodec copy %06d.jpg
```  
  
### Play ugoira on smartphone?
  Install mpv player  
  Open mpv -> Settings -> Advanced ->  Edit mpv.conf -> type loop -> SAVE  
  copy ugoira to smartphone and play.  
  
### Art filename
By default, the art will be saved like ```art-title_001.jpg```, and if already exist, will be ```art-title(art-id)_001.jpg```  
  
if want to save like ```art-id_001.jpg```, change the follow:  
extraction.py  
SAVE_FORMAT = 0  
to  
SAVE_FORMAT = 1  

### Clipboard pickup + yt-dlp
Liked the clipboard url pickup?  
a bonus script ./opt/clipget.py can be used with yt-dlp.  
```
./clipget.py
(copy what you want)
Ctrl+C
```
‘dllist’ will be created in the same directory as clipget.py  
```
cat ./dllist | xargs yt-dlp
``` 

### How to make lossless ugoira(for developer)

Format: VFR mjpeg  

How to:  
1. Download ugoira.zip and ugoira_meta(the frame rate information is here)  
2. make mjpeg video: ffmpeg -i ugoira/%06d.jpg -vcodec copy ugoira_pre.mp4
```
note: ffmpeg may skip the 1st frame when play.

      make video with this:
      000001.jpg(1000ms)  000002.jpg(1000ms)  000003.jpg(1000ms) 

      play like:
      000002.jpg -> wait 1000ms -> 000003.jpg -> wait 1000ms

      solution of pixiv-extraction is to make a copy of 1st frame:
      000001.jpg(1ms)  000002.jpg(1000ms)  000003.jpg(1000ms)  000004.jpg(1000ms) 

      000001.jpg and 000002.jpg is identical.
```
3. make timecode.txt from ugoira_meta  
4. VFR the video: mp4fpsmod -o ugoira.mp4 -x -t timecode.txt ugoira_pre.mp4  
5. Play ugoira with mpv  
      

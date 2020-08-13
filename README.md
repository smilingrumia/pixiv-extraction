[README(日本語)](https://github.com/smilingrumia/pixiv-extraction/blob/master/README(%E6%97%A5%E6%9C%AC%E8%AA%9E).md)  
# pixiv-extraction

Simple,quick and lossless([*detail](#detail-of-lossless)) download automation script.  
To download Pixiv images and Ugoira(Pixiv's animated image)  

OS: Linux,Windows10  
Version: v0.7.6  

###### use with respect at their server, Cheers.


Overview
===========================
- [Install](#Instalation)
	- [pixiv-extraction](#install-pixiv-extraction)
	- [mpv](#install-mpv)
	- [Optionals](#install-optionals)
- [Run](#run)
- [Notes](#notes)
	- Detail of lossless
	- Play ugoira on smartphone?
	- Want to DL all art of the artist, but lazy to click all of them?
	- Art filename format
	- MAYBE: is better NOT logout via pixiv web page(this may disable the cookie?)
	- Clipboard-mode URL pickup + youtube-dl
	- Remove  ‘Email Image’ from firefox  New!
	- In future, when pixiv make change in their site
- [Change log](#change-Log)
----------------------------

 
# Instalation  
  
The follow are tested on Linux(Ubuntu 16.04)  
For Windows10 see :
[README(Windows10)](https://github.com/smilingrumia/pixiv-extraction/blob/master/README(Windows10).md)  

## install pixiv-extraction
**Clone the source**

```
git clone https://github.com/smilingrumia/pixiv-extraction   
```

**Install the Dependency**  
```
sudo apt update
sudo apt install curl p7zip-full ffmpeg python3-tk python3-brotli
```

Install mp4fpsmod:  
Open [mp4fpsmod github](https://github.com/nu774/mp4fpsmod) -> Release -> DL the latest(here will be 0.26)
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

### Copy your http header to  httpHeader/
Now, We will need your login-credential(Cookie) to get the art.  
  
Is better to create an account only for this purpose because:  
1.login-credential(Cookie) will be stored in plain text in httpHeader/.  
2.if something goes wrong and the program end up leaking your cookie?  
3.if pixiv decides to ban due to fast-downloading?  
if you use your account only for viewing, and don’t might to recreate, may be OK.  
  
So beginning...  
as browser, Firefox will be used.
  
**Step 1**  
Login to Pixiv(With a lost-ok account)  
Open an art  
Address bar will look like:  ```https://www.pixiv.net/en/artworks/12345678```  
  
F12(open devtool) -> Network tab -> F5/Refresh the Pixiv page  
A list in Network tab will be displayed.  
May be on the top,  
select: Domain(```www.pixiv.net```) File(12345678) Type(html)  
  
On the right window, goto Headers-> Request Headers  
Turn ON Raw headers  
Right Click -> select all -> Right Click -> copy  
  
Open httpHeader/pixiv_artpage with text-editor and paste your header    
(This Header must contain Cookie)  
  
Save it.  
  
**Step 2**  
Next in Network tab  
select one with: Type(json)  
And like Step 1, copy&pasete the header to httpHeader/pixiv_artlist  
(This Header must contain Cookie and x-user-id)  
  
Save it.  
  
Close the devtool.  
  
**Step 3**  
Open some art(picture)  
Right click 1 image -> Open link in new window  
Address bar will look like: ```https://i.pximg.net/img-original/img/2016/01/02/03/04/05/12345678_p0.png```  
  
F12(open devtool) -> Network tab -> F5/Refresh the Pixiv page  
On Network tab, select: Domain(```i.pixiv.net```) File(12345678_p0.png)  
and copy&paste the header to httpHeader/pixiv_art  

if contain follow, EXCLUDE THAT LINE!
```
If-Modified-Since: <something>
Range: <something>
If-Range: <something>
```

(This Header DON’T contain Cookie or x-user-id)  
  
Save it.  


## install mpv
mpv is a good media player, that will play ugoira smoothly.  
Install the latest mpv.  
like mpv(0.30.0) should play smooth, VFR Compatible, and no “title flicking”  
!! On Ubuntu 16.04, if mpv are installed from default repository, will be old(0.14.0) and fail to play as VFR!!  

***via ppa(Easiest way)***
```
sudo add-apt-repository ppa:mc3man/mpv-tests
sudo apt update
sudo apt install mpv

# check
mpv --version

# Optional: you can remove the ppa once mpv are installed.
```

***via mpv-build***  
```
# Dependency(for ubuntu 16.04)
sudo apt install python-minimal libssl-dev libfribidi-dev libluajit-5.1-dev libx264-dev libegl1-mesa-dev \
git autoconf libtool nasm xorg-dev libglu1-mesa-dev libvdpau* libpulse-dev \
   libass-dev libavresample-dev libalsa-ocaml-dev liblcms2-dev libluajit-5.1-dev libjpeg-dev

# Clone source
git clone https://github.com/mpv-player/mpv-build.git
cd mpv-build

# Enabling optional ffmpeg dependencies
echo --enable-libx264 >> ffmpeg_options

./rebuild -j4
sudo ./install

# Check
mpv –version
```

**Configure mpv to be confortable**  
nano ~/.config/mpv/mpv.conf  
```
# Change this for better performance on general use.
#hwdec=vdpau
#vo=vdpau

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
nano ~/.config/mpv/input.conf  
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

## install Optionals

**apparmor(Advanced and Optional)**
```
# Modify it, to suit your environment
nano  pixiv-extraction/.opt/apparmor-profile

sudo cp pixiv-extraction/.opt/apparmor-profile /etc/apparmor.d/pixiv-extraction
sudo apt install apparmor-utils
sudo aa-enforce /etc/apparmor.d/pixiv-extraction

# check
sudo aa-status | grep -z pixiv
```

**Image viewer(Optional)**  
Image viewer Can be anything, mirage is the suggested one here.  
```
sudo apt install mirage
``` 


# Run  
**Normal mode**  
```./extraction.py <url1> <url2> ...```  
  
this will look like  
```./extraction.py https://www.pixiv.net/en/artworks/12345678 https://www.pixiv.net/en/artworks/23456789 ...```  
  
   
**Clipboard mode**  
```./extraction.py -c```  
  
Copy art URL to clipboard.  
open pixiv with browser, if are using firefox, right click -> a on the art thumbnail.  
copied URL shuld look like: ```https://www.pixiv.net/en/artworks/12345678```  
Do this on all art that you want.  

Ctrl+C on the terminal  
if the list looks ok, type y and Enter.  

Important: Recent firefox has an option called 'Email Image' that conflict with right click -> a.  
See "Remove ‘Email Image’ from firefox" on Notes.  
  
To see version, just Run ./extraction.py  

**Where is saved?**  
Images: save_images/  
Ugoira: save_ugoira/  
  
# Notes  
### Detail of lossless
  
**Images**  
 Original images are just downloaded.  
  
**Ugoira**  
 In short, is a VFR mjpeg as .mp4 that mpv can play.  
 is NOT gif, apng, webm or lossy mp4.  

 .mp4 will be make using original Ugoira images,  
 with NO re-encoding or such thing.  
 And  can be reversed to original images with:  
 ```
 ffmpeg -i ugoira.mp4 -vcodec copy %06d.jpg
 ```
  
  One more thing is that Ugoira is VFR(variable frame rate) by design.  
  And some part of Ugoira(10-20% maybe?)  are made as VFR,  
  pixivi-extraction can handle VFR, thanks to mp4fpsmod!  
  
### Play ugoira on smartphone?
  Install mpv player  
  Open mpv -> Settings -> Advanced ->  Edit mpv.conf -> type loop -> SAVE  
  copy ugoira to smartphone and play.  

### Want to DL all art of the artist, but lazy to click all of them?
  A lazy solution was done, see .otp/pageToUrl.js 
  (not sure how to do ‘cat dllist | xargs ./extraction.py’ on windows) 
  
### Art filename format
By default, the art will be saved like ```art-title_001.jpg```, and if already exist, will be ```art-title(art-id)_001.jpg```  
  
if want to save like ```art-id_001.jpg```, change the follow:  
extraction.py  
SAVE_FORMAT = 0  
to  
SAVE_FORMAT = 1  
  
### MAYBE: is better NOT  logout via pixiv web page(this may disable the cookie?)
In case that pixiv-extraction are working, but after logout via pixiv web page aren't working,  
Do the Step 1 to 3, and to “logout”, clean the pixiv cookie via browser.  

### Clipboard-mode URL pickup + youtube-dl
Liked the clipboard-mode URL pickup?  
A bonus script on ./opt/clipget.py, can help youtube-dl(a [wide-range sites](https://ytdl-org.github.io/youtube-dl/supportedsites.html) downloader).  
run:  
```
./clipget.py
(copy what you want)
Ctrl+C
```
the list will be saven as ‘dllist’ on same directory as clipget.py.  
Then run something like:  
```
cat ./dllist | xargs youtube-dl -f best
```
### Remove ‘Email Image’ from firefox
On firefox, when Right Click -> A on a image(to get the link URL quickly)  
recent firefox have an option called ‘Email Image...’, that conflict with this shortcut-key.  

If remove ‘Email Image...’, Right Click -> A on a image will easly copy the URL.(a huge difference to who frequently/many downloads)  
The follow are how to remove ‘Email Image ’ from firefox.  

about:config  
'''
toolkit.legacyUserProfileCustomizations.stylesheets=true
'''

On firefox profile directory (<something>mozilla/firefox/<something>.default/) 
create chrome/userChrome.css
'''
@namespace url("http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul");

#context-sendimage { display:none!important; }
'''

Restart and check if worked.  

### In future, when pixiv make change in their site
This programs probably will stop to work with some error message, And have to be updated to continue to work.  
In that case, when I detect the change, I will announce the situation here, and hopefully fix it if I can.

# Change Log
```
 v0.7.6
  clipboard listening improve(non-pixiv URL will be ignored)
  bonus in .opt/clipget.py, clipboard-mode pickup that helps youtube-dl(see in Notes)
  
 v0.7.5
  fix some art title(< and >)
  lazy solution to easly download all arts of artist
  
 v0.7.4
  improve clipboard detection speed
  fix some art title
  other small improve
  
 v0.7.3
  Windows10 support
  
 v0.7.2
  remove: saving art info to save_images/info and save_ugoira/info
  modify: output message
  
 v0.7.1
  fix: auto clean of ugoira temporary data
  fix: support for "Accept-Encoding: gzip, br"
  other small fix/changes

 v0.7.0  
   Some Ugoira are VFR(variable frame rate), so VFR implementation was done  
   bug-fix: If clipboard are empty and run as clipboard-mode, it will crash  
   bug-fix: ffmpeg are skipping the first frame
   other small fix/changes  
   
 v0.6.0  
   Publish  
```
      

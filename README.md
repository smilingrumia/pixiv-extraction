# pixiv-extraction

Quick and lossless([detail](https://github.com/smilingrumia/pixiv-extraction/#user-content-detail-of-lossless)) download automation script in python3 for Linux  
To download Pixiv images and Ugoira(Pixiv's animated image)  
  
Version: v0.7.0  

###### use with respect at their server, Cheers.
 
# Instalation  
  
(The follow are tested on Ubuntu 16.04)  

**Clone the source**

```
git clone https://github.com/smilingrumia/pixiv-extraction   
```


**Install the Dependency**  
curl:       for http/https comunication  
7-zip:         for unzip Ugoira  
ffmpeg:     for lossless conversion of ugoira(images) to mp4  
python3-tk: for clipboard downloading mode  
python3:    if don’t have, install it too  
mp4fpsmod:  to make a VFR mp4  
  
```
sudo apt update
sudo apt install curl p7zip-full ffmpeg python3-tk
```

Install mp4fpsmod:  
Open [mp4fpsmod github](https://github.com/nu774/mp4fpsmod) -> Release -> DL the latest(here will be 0.26)
```
tar xf mp4fpsmod-0.26.tar.gz
cd mp4fpsmod-0.26
./bootstrap.sh
./configure
make

# move compiled binary to pixiv-extraction/
mv ./mp4fpsmod <path>/pixiv-extraction/
```

**apparmor security enforcing(Optional)**
```
# Modify it, to suit your environment
nano  pixiv-extraction/.opt/apparmor-profile

sudo cp pixiv-extraction/.opt/apparmor-profile /etc/apparmor.d/pixiv-extraction
sudo apt install apparmor-utils
sudo aa-enforce /etc/apparmor.d/pixiv-extraction

# check
sudo aa-status | grep -z pixiv
```
  
## Copy your http header to  httpHeader/
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
  
Modify the:  
Accept-Encoding: gzip, deflate, br  
to  
Accept-Encoding: deflate, br  
  
Save it.  
  
**Step 2**  
Next in Network tab  
select one with: Type(json)  
And like Step 1, copy&pasete the header to httpHeader/pixiv_artlist  
(This Header must contain Cookie and x-user-id)  
  
Modify the:  
Accept-Encoding: gzip, deflate, br  
to  
Accept-Encoding: deflate, br  
  
Save it.  
  
Close the devtool.  
  
**Step 3**  
Open some art(picture)  
Right click 1 image -> Open link in new window  
Address bar will look like: ```https://i.pximg.net/img-original/img/2016/01/02/03/04/05/12345678_p0.png```  
  
F12(open devtool) -> Network tab -> F5/Refresh the Pixiv page  
On Network tab, select: Domain(```i.pixiv.net```) File(12345678_p0.png)  
and copy&paste the header to httpHeader/pixiv_art  
if contain 'If-Modified-Since' exclude that line.  
(This Header DON’T contain Cookie or x-user-id)  
  
Save it.  
  
# Run  
**Normal mode**  
```./extraction.py <url1> <url2> ...```  
  
this will look like  
```./extraction.py https://www.pixiv.net/en/artworks/12345678 https://www.pixiv.net/en/artworks/23456789 ...```  
  
   
**Clipboard mode**  
```./extraction.py -c```  
  
Beginning Copy the arts url with: Right Click -> a  
Copied URL shuld look like: ```https://www.pixiv.net/en/artworks/12345678```  
  
Ctrl+C on the terminal  
if the list looks ok, type y and Enter.  
  
To see version, just Run ./extraction.py  

**Where is saved?**  
Images: save_images/  
Ugoira: save_ugoira/  
  
# Notes  
### Detail of lossless
  
**Images**  
 Original images are just downloaded.  
  
**Ugoira**  
 .mp4 will be make using original Ugoira images,  
 with NO re-encoding or such thing.  
  And  can be reversed to original images with:  
 ```
 ffmpeg -i ugoira.mp4 -vcodec copy %06d.jpg
 ```
  
  One more thing is that Ugoira is VFR(variable frame rate) by design.  
  And some part of Ugoira(10-20% maybe?)  are made as VFR,  
  pixivi-extraction can handle VFR(thanks to mp4fpsmod!)  
  
### Player for Ugoira
Install the latest mpv.  
Run:  
```
mpv --loop --idle=yes --force-window
```
like mpv(0.30.0) should play smooth, VFR Compatible, and no “title flicking”  
!! On Ubuntu 16.04, if mpv are installed with apt will be old(0.14.0) and fail to play as VFR!!  

### Image viewer
If want to try, I suggest mirage.
```
sudo apt install mirage
``` 
  
### Art filename
By default, the art will be saved like ```art-title_001.jpg```, and if already exist, will be ```art-title(art-id)_001.jpg```  
  
if want to save like ```art-id_001.jpg```, change the follow:  
extraction.py  
SAVE_FORMAT = 0  
to  
SAVE_FORMAT = 1  
  
### MAYBE: is better NOT  logout via pixiv web page(this may disable the cookie?)
In case that pixiv-extraction are working, but after logout via pixiv web page aren't working,  
Do the Step 1 to 3, and to “logout”, clean the pixiv cookie via browser.  
  
### Clean-up manually tmp/ in a while
tmp/ folder is used to store ugoira temporary data, and all file inside(not tmp/ itself) can be deleted on the end of program.   
~~The author was scared to use folder deletion API~~ this may be fixed in future.
  
### In future, when pixiv make change in their site
This programs probably will stop to work with some error message, And have to be updated to continue to work.  
In that case, when I detect the change, I will announce the situation here, and hopefully fix it if I can.

# Change Log
```
 v0.7.0  
   Some Ugoira are VFR(variable frame rate), so VFR implementation was done.  
   bug-fix: If clipboard are empty and run as clipboard-mode, it will crash.  
   other small fix/changes.  
   
 v0.6.0  
   Publish.  
```
      

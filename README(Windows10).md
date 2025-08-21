# Install instruction for Windows 10  

**pixiv-extraction**  
  1.Download and unzip 

**Python3**  
  1.Download the installer: https://www.python.org  
  2.Start  
  3.Customise installation  
     Confirm that follow are selected(if by default all are selected, it's OK)  
     pip  
     td/tk and IDLE  
  4.Next  
  5.Install  

**Python3 brotli**  
  1.open cmd(command-prompt)  
  2.py -3 -m pip install brotli  

**7-zip**  
  1.Download 7-zip: https://www.7-zip.org/  
  2.Install  
  3.Open C:\Program Files\7-Zip  
  4.Select all files, and copy inside of pixiv-extraction  

**curl**  
  1.Download curl: https://curl.haxx.se/windows/  
  2.Unzip  
  3.Open curl-7.70.0-win64-mingw\bin  
  4.Select all files, and copy inside of pixiv-extraction  

**ffmpeg**  
  Official site:  https://www.ffmpeg.org/download.html  

  1.Download ffmpeg: https://ffmpeg.zeranoe.com/builds/  
  2.Select   
    v4.2.2  
    Windows64-bit(if yor machine is 64bit)  
    Static  
  3.Download Build  
  4.Unzip  
  5.Open ffmpeg-4.2.2-win64-static\bin  
  6.Select all files, and copy inside of pixiv-extraction  

**mp4fpsmod**  
  1.Download mp4fpsmod: https://github.com/nu774/mp4fpsmod/releases
  2.Unzip  
  3.Move mp4fpsmod.exe to pixiv-extraction  


**mpv**  
  Official site: https://mpv.io/installation/  

  1.Download mpv-x86_64-20200510-git-4e94b21.7z: https://sourceforge.net/projects/mpv-player-windows/files/  
  2.Decompress with 7-zip  
  3.Open mpv-x86_64-20200510-git-4e94b21\installer  
  4.Right click on mpv-install, Rum as Administrator and Install  

  5.Open notepad and copy the follow  
```
UP       add volume 5
DOWN     add volume -5
n        playlist-next
p        playlist-prev
```

  6.Save as  
    file path: C:\Users\<YOUR USERNAME>\AppData\Roaming\mpv  
    file name: input.conf  
    file type: all file  

  7.Open notepad and copy the follow  
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
  8.Save as  
    file path: C:\Users\<YOUR USERNAME>\AppData\Roaming\mpv  
    file name: mpv.conf  
    file type: all file  


**How to display video thumbnail**  
Program to make mp4 thumbnail may need.  
have various, here we will try Media Preview.  

Media Preview  
Official: http://www.babelsoft.net/products/mediapreview.htm  
Third Party(https): https://www.free-codecs.com/download/media_preview.htm  

1.Download  
2.Install  
3.Media Preview configuration will popup(if not open)  
4.Video Formats -> check .mp4 -> Apply -> Exit  


**Next thing to do**  
Go back to README.md and follow "Copy your http header to httpHeader/"

to run, do like this 
```
 # Open cmd
 
 # note: 'right click' on cmd, can paste(like Ctrl + V)
 cd C:\Users\<USER NAME>\Desktop\pixiv-extraction\

 # note that in windows dont need to start with ./ like linux
 extraction.py -c
```

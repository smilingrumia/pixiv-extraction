[README(English)](https://github.com/smilingrumia/pixiv-extraction)  

# 重要
**Pixiv側のアップデートにより、現在このスクリプトは使用不可です。  
使用出来るようにリメイクする予定ですが、しばらく時間が掛かるかもしれません。  **

In any case,  
The teck to make lossless ugoira is:  
1. Download ugoira.zip and ugoira_meta(the frame rate information is here)  
2. make mjpeg video: ffmpeg -i ugoira/%06d.jpg -vcodec copy ugoira_pre.mp4  
3. make timecode.txt from ugoira_meta  
4. VFR the video: mp4fpsmod -o ugoira.mp4 -x -t timecode.txt ugoira_pre.mp4  
5. Play ugoira with mpv  

# pixiv-extraction

シンプルで無劣化（[詳細](#無劣化の詳細)）のPixiv画像とうごイラのダウンロードツール。   

OS: Linux,Windows10  
Version: v0.7.6  

このREADMEは主にLinuxを対象としています、  
Windowsの方なら部分的に違いがあるので、[README(Windows10)](https://github.com/smilingrumia/pixiv-extraction/blob/master/README(Windows10).md)もお読みください。  

Overview
===========================
- [インストール](#インストール)
	- [pixiv-extraction](#pixiv-extractionのインストール)
	- [mpv](#mpvのインストール)
	- [その他](#その他のインストール)
- [実行](#実行)
- [Notes](#notes)
	- '画像をメールで送信する'をfirefoxから取り除く
	- 無劣化の詳細
	- スマホでうごイラを再生する方法
	- Want to DL all art of the artist, but lazy to click all of them?
	- Art filename format
	- 多分: Pixiv経由でログアウトするとクッキーが解除される恐れがあります
	- Clipboard-mode URL pickup + youtube-dl
	- 将来pixivのウェブページの仕様が変更になった時
- [Change log](#change-Log)
----------------------------

 
# インストール  
 
## pixiv-extractionのインストール
**本ソフトのダウンロード**

```
git clone https://github.com/smilingrumia/pixiv-extraction   
```

**依存性のインストール**  
```
sudo apt update
sudo apt install curl p7zip-full ffmpeg python3-tk python3-brotli
```

mp4fpsmodのインストール:  
[mp4fpsmod](https://github.com/nu774/mp4fpsmod)のgithubを開く -> Releases -> 最新をDL(ここでは0.26)
```
# コンパイルに必要になるかもしれない依存性
sudo apt install autoconf libtool

tar xf mp4fpsmod-0.26.tar.gz
cd mp4fpsmod-0.26
./bootstrap.sh
./configure
make

# コンパイルしたバイナリをpixiv-extraction/に移動
mv ./mp4fpsmod <path>/pixiv-extraction/  
```

### あなたのHTTPヘッダーをhttpHeader/にコピー
アートの取得には、あなたのPixivのログイン情報（Cookie）が必要です。  
  
以下の理由により専用のアカウントを作るのがベターです。  
1.ログイン情報(Cookie)が平文（暗号化されずに）httpHeader/に保存される為.  
2.もしも誤った事が起きてクッキーが漏れたら？   
3.もしもPixivがダウンローダーを使った事でBANしたら？  
ただし、ほぼ閲覧しかしないアカウントや失っても再作成すれば良い方なら多分大丈夫だと思います。  
  
それでは以下の手順でhttpヘッダーをコピーしましょう、ブラウザはFirefoxを使います。  
  
**Step 1**  
ピクシブにログイン  
アート（画像）を一つ開く  
アドレスバーはこんな感じになるはず:  ```https://www.pixiv.net/artworks/12345678```  
  
F12(開発ツールを起動) -> ネットワーク -> F5/リフレッシュ  
 
「ネットワーク」タブにリストが表示されます  
多分一番上にある: ドメイン(```www.pixiv.net```) ファイル(12345678) タイプ(html)　を選択  

右のウィンドウの ヘッダー-> 要求ヘッダー　へ行き
生ヘッダーをONにします。  
内容を右クリック -> すべてを選択 -> 右クリック -> コピー  
  
httpHeader/pixiv_artpageをテキストエディタで開き、コピーしたヘッダーを貼り付けます。  
(このヘッダーにはCookieが含まれている必要があります)  
  
保存。 
  
**Step 2**  
ネットワークタブで、右のを一つ選択: タイプ(json)  
ステップ１のように、ヘッダーをhttpHeader/pixiv_artlistにコピー＆ペース  
(このヘッダーにはCookieとx-user-idが含まれている必要がアリます)  
  
保存。  
  
開発ツールを一旦閉じる。  
  
**Step 3**  
アート（画像）を一つ開きます  
画像を右クリック-> リンクを新しいウィンドウで開く  
アドレスバーは右のようになるべきです: ```https://i.pximg.net/img-original/img/2016/01/02/03/04/05/12345678_p0.png```  
  
F12(開発ツールを開く) -> ネットワーク -> F5/リフレッシュ 
「ネットワーク」タブで右を選択: ドメイン(```i.pixiv.net```) ファイル(12345678_p0.png)  
ステップ１のように、ヘッダーをhttpHeader/pixiv_artにコピー＆ペース  

以下の行があれば、その行を削除して下さい。
```
If-Modified-Since: <something>
Range: <something>
If-Range: <something>
``` 

(このヘッダにはCookieもx-user-idも含まれません)  
  
保存。  


## mpvのインストール
mpvは本ソフトで作成したうごイラもスムーズに再生できるgoodなプレイヤーです。  
最新のmpvをインストールしましょう。  
最新のmpvはppa,[mpv-build](https://github.com/mpv-player/mpv-build)または手動で[mpv](https://github.com/mpv-player/mpv)をビルドしてインストール出来ます。  

***ppa(簡単な方法)***
```
sudo add-apt-repository ppa:mc3man/mpv-tests
sudo apt update
sudo apt install mpv

# check
mpv --version

# Optional: you can remove the ppa once mpv are installed.
```

**快適なうごイラ再生の為の、mpvの設定**  
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

**mpvの基本的なコマンド**  
```
 n          next video     (複数の動画をmpvにドラッグ＆ドロップした時に有効です)
 p          previous video (複数の動画をmpvにドラッグ＆ドロップした時に有効です)
 UP         volume up
 DOWN       volume down
 RIGHT      5sec next
 LEFT       5sec back
 Alt+RIGHT  right rotate
 Alt+LEFT   left rotate
 f          full screen
 q          quit
```

## その他のインストール

**イメージビューアー(スキップ可)**  
mirageも良いビューアーです。  
```
sudo apt install mirage
``` 
もしLinuxが英語環境で画像表示の順番がおかしい場合は、  
以下の様にmirageを起動すると良いかもしれません。  
一時的な解決法    
```
LANG=ja_JP.UTF-8 /usr/bin/mirage
```
永続的な解決方（ラッパーを作成）  
sudo nano /usr/local/bin/mirage
```
#!/bin/bash

LANG=ja_JP.UTF-8 /usr/bin/mirage "${1}"
```
sudo chmod 755 /usr/local/bin/mirage

# 実行
**ノーマル・モード**  
```./extraction.py URL1 URL2 ...```  

実際には以下のようになります:   
```./extraction.py https://www.pixiv.net/en/artworks/12345678 https://www.pixiv.net/en/artworks/23456789 ...```  
  
   
**クリップボード・モード**  
```./extraction.py -c```  
  
'./extraction.py -c'を実行  
Pixivをブラウザで開き、firefoxならDLしたい画像を右クリック->AでURLをコピー。  
コピーしたURLは: ```https://www.pixiv.net/artworks/12345678```  
DLしたいアートを次々コピーしましょう。  

DLの開始には、  
ターミナルでCtrl+C、問題なければyとEnterを押しましょう。  

**重要**: 最近のfirefoxは'画像をメールで送信する'ようなオプションがあり、  
これが右クリック->Aとバッティングしてしまいます。  
'画像をメールで送信する'オプションをfirefoxから取り除く方法をNotesで解説しています。  
  
バージョンを見たければ、シンプルに./extraction.py  

**保存場所**  
画像: save_images/  
うごイラ: save_ugoira/  
  
# Notes  
### '画像をメールで送信する'をfirefoxから取り除く
'画像をメールで送信する'をfirefoxから取り除いた場合、  
クリップボードモードで本ソフトを起動し、DLしたい画像を右クリック->AだけでDL予定リストに入れる事が出来ます。  
'画像をメールで送信する'が残ったままだと右クリック->A->Enterと不便です。  

以下が取り除く方法です  

about:config  
```
toolkit.legacyUserProfileCustomizations.stylesheets=true
```

firefoxのプロファイルディレクトリにて(<something>mozilla/firefox/<something>.default/)  
chrome/userChrome.cssを作成  
```
@namespace url("http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul");

#context-sendimage { display:none!important; }
```
firefoxを再起動して確認。  

### 無劣化の詳細
  
**画像**  
オリジナル画像がダウンロードされます。 
  
**うごイラ**  
うごイラは、複数のjpeg画像とフレームレート情報から成り立ちます。  
１画像毎に何ミリ秒待つかが設定されているのでVFR（可変フレームレート）です。  

本ソフトでは、オリジナルのjpegを使ってmjpeg形式の動画（便宜上.mp4）を作り、mp4fpsmodでVFR化します。  
画質とフレームレートともに無劣化です。  
本ソフトで作成するのはgif,apng,webmでも劣化mp4でもありません。  

以下のコマンドでオリジナル画像への復元も可能です。  
```
ffmpeg -i ugoira.mp4 -vcodec copy %06d.jpg
```
  
### スマホでうごイラを再生する方法
  mpv playerをスマホにインストール。  
  mpv -> Settings -> Advanced ->  Edit mpv.conf -> loopと入力 -> SAVE  
  うごイラをスマホにコピーして再生。 

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
  
### 多分: Pixiv経由でログアウトするとクッキーが解除される恐れがあります
pixiv-extractionが正常動作していても、ログアウト後に動作しなくなった場合はこれが疑わしいです。  
その場合httpヘッダーをもう一度コピーしなおして、ブラウザ側でクッキーを削除すれば”ログアウト”が出来ます。  

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

### 将来pixivのウェブページの仕様が変更になった時
おそらく何らかのエラーメッセージを表示してダウンロードは失敗します。  
その時は状況をここでアナウンスし、可能であればfixする予定です。  

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
      

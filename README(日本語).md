[README(English)](https://github.com/smilingrumia/pixiv-extraction)  

# pixiv-extraction

高速で無劣化/高画質（[*詳細](https://github.com/smilingrumia/pixiv-extraction/blob/master/README%28%E6%97%A5%E6%9C%AC%E8%AA%9E%29.md#Notes)）の
Pixiv「画像」と「うごイラ」のダウンローダーです。  

OS: Linux,Windows10  
Version: v0.7.4  

###### サーバーをリスペクトしつつ使いましょう, Cheers.
 
# インストール
  
以下の手順はLinux(Ubuntu 16.04)で確認  
Windows10はこちらを参考に:
[README(Windows10)](https://github.com/smilingrumia/pixiv-extraction/blob/master/README(Windows10).md)  

**本ソースのクローン**

```
git clone https://github.com/smilingrumia/pixiv-extraction   
```


**依存性**  
curl:　http/https通信  
7-zip: うごイラの解凍  
ffmpeg: うごイラをmp4に変換  
python3-tk: 「クリップボード・ダウンロード」モード  
python3:　このスクリプトはpython3なので、もし未インスールであればこちらも  
mp4fpsmod:  VFR(可変フレームレート)なうごイラ.mp4を作成  
python3-brotli: "Accept-Encoding: br"のデコード  
  
```
sudo apt update
sudo apt install curl p7zip-full ffmpeg python3-tk python3-brotli
```

mp4fpsmodのインストール:  
[mp4fpsmod github](https://github.com/nu774/mp4fpsmod)を開く -> Release -> 最新をDL(ここでは0.26)
```
#  依存性
sudo apt install autoconf libtool

tar xf mp4fpsmod-0.26.tar.gz
cd mp4fpsmod-0.26
./bootstrap.sh
./configure
make

# コンパイルしたバイナリをpixiv-extraction/に移動
mv ./mp4fpsmod <path>/pixiv-extraction/
```

**apparmor(上級者向け、スキップ可)**
```
# 各環境に適応するように編集
nano  pixiv-extraction/.opt/apparmor-profile

sudo cp pixiv-extraction/.opt/apparmor-profile /etc/apparmor.d/pixiv-extraction
sudo apt install apparmor-utils
sudo aa-enforce /etc/apparmor.d/pixiv-extraction

# 確認
sudo aa-status | grep -z pixiv
```

**イメージビューアーのインストール(スキップ可)**  
どのビューアーでも大丈夫ですが、ここではmirageがおすすめです。  
```
sudo apt install mirage
```

**うごイラ用のプレイヤーのインストール**  
最新のmpvをインストールしてください。  
例えばmpv(0.30.0)はスムーズ、VFR、"タイトルがちらつく現象"も無く快適です。  
!!Ubuntu16.04の場合、デフォルトのリポジトリからインストールすると古いため（0.14.0）VFRに失敗します!!  

**ppaを使ってインストール（一番簡単です）**  
```
sudo add-apt-repository ppa:mc3man/mpv-tests
sudo apt update
sudo apt install mpv

# check
mpv --version

# インストール後はppaを無くしても大丈夫です。
```

**mpv-buildを使ってインストール**  
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

**快適な動作の為の設定**  
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
UP		add volume 5
DOWN	add volume -5
n		playlist-next    
p		playlist-prev
```

**mpvのベーシックなコマンド**
```
 n          next video
 p          previous video
 UP         volume up
 DOWN       volume down
 RIGHT      5sec next
 LEFT       5sec back
 Alt+RIGHT  right rotate
 Alt+LEFT   left rotate
 f          full screen
 q          quit
```
  
## httpヘッダーをhttpHeader/へコピー
アートの取得には、あなたのPixivのログイン情報（Cookie）が必要です。  
  
以下の理由により専用のアカウントを作るのがベターです。  
1.ログイン情報(Cookie)が平文（暗号化されずに）httpHeader/に保存される為.  
2.もしも誤った事が起きてクッキーが漏れたら？   
3.もしもPixivがダウンローダーを使った事でBANしたら？  
ただし、ほぼ閲覧しかしないアカウントや失っても再作成すれば良いよ、という人なら多分大丈夫だと思います。  
  
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

(このヘッダにはCookieもx-user-idも**含まれません**)  
  
保存。  
  
# 実行  
**ノーマル・モード**  
```./extraction.py <url1> <url2> ...```  
  
実際は以下のようになります  
```./extraction.py https://www.pixiv.net/en/artworks/12345678 https://www.pixiv.net/en/artworks/23456789 ...```  
  
   
**高速なクリップボード・モード**  
```./extraction.py -c```  
  
ダウンロードしたいアートのコピーを開始（右クリック -> aで楽に出来ます）  
コピーされたURLはこのフォーマットです: ```https://www.pixiv.net/artworks/12345678```  
  
ターミナルでCtrl+C。  
良さそうであればyとEnter.  
  
バージョンを確認するには./extraction.py  

**保存先**  
画像: save_images/  
うごイラ: save_ugoira/  
  
# Notes  
### 無劣化・高画質の詳細
  
**画像**  
 オリジナル画像がダウンロードされます。  
  
**うごイラ**  
 オリジナル画像がダウンロードされて、mp4に変換されます。  
 再エンコード等は一切されませんし、以下のコマンドでオリジナル画像への復元も可能です。  
 ```
 ffmpeg -i ugoira.mp4 -vcodec copy %06d.jpg
 ```
 
もう一つ重要なのが、うごイラはVFR（可変フレームレート）形式という事です。  
実際には10-20%程？のうごイラはVFRとして作成されています。  
pixivi-extractionはVFRに対応しています！ mp4fpsmodのおかげです、感謝！  
  
### 保存先ファイル名
デフォルトでは ```タイトル_001.jpg```か、すでに存在していれば```タイトル(アートID)_001.jpg```となります。  
```アートID_001.jpg```のように保存したければ以下を編集してください。  
extraction.py  
SAVE_FORMAT = 0  
を以下のように  
SAVE_FORMAT = 1  
  
### 多分: Pixiv経由でログアウトするとクッキーが解除される恐れがあります
pixiv-extractionが正常動作していても、ログアウト後に動作しなくなった場合はこれが疑わしいです。  
その場合httpヘッダーをもう一度コピーしなおして、ブラウザ側でクッキーを削除すれば”ログアウト”が出来ます。  

### 将来pixivのウェブページの仕様が変更になった時
おそらく何らかのエラーメッセージを表示してダウンロードは失敗します。  
その時は状況をここでアナウンスし、可能であればfixする予定です。  

# Change Log
```
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
      

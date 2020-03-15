# gmail_picamera
Raspberry Piで作るGmailで操作するPiCamera<br>
![動作例](https://github.com/y-tetsu/gmail_picamera/blob/master/image/circle2.gif)

## 概要
Gmailの自分のメールアドレスにスマホなどから指令を送ると、カメラ撮影を開始し、動画を指令元へ送り返すRaspberry Piを使った装置。

## 動作確認環境
- Raspbian GNU/Linux 9.8 (stretch)
- Python3.5.3
    - picamera
    - RPi.GPIO
    - pigpio
    - google-api-python-client
    - google-auth-oauthlib
    - oauth2client

## 必要機材
- ラズベリーパイ : Raspberry Pi 3 Model B    × 1
- ACアダプタ                                 × 1
- 32GB SDカード                              × 1
- ケース                                     × 1
- カメラ : Raspberry Pi Camera Module V2     × 1
- サーボモータ : SG90                        × 2
- カメラマウント                             × 1
- 抵抗1KΩ                                   × 2
- ジャンパー線                               × 適量

## 機器接続図
![接続図](https://github.com/y-tetsu/gmail_picamera/blob/master/image/connection.png)

## 使い方
### pigpioのセットアップ
事前に下記を実行しデーモンを立ち上げる。<br>
```
$ sudo pigpiod
```

### h264形式をmp4に変換できるようにする
下記でソフトをダウンロードする。<br>
```
$ sudo apt-get update
$ sudo apt-get install -y gpac
```

### Gmail APIを有効化する
Gmail APIの使用に必要なパッケージをインストールする。<br>
```
pip3 install --upgrade google-api-python-client
pip3 install --upgrade google-auth-oauthlib
pip3 install --upgrade oauth2client
```
[Gmail APIとPythonを使ってメール送信を自動化する方法](https://valmore.work/automate-gmail-sending/)を参照してGoogle Cloud PlatformでGmail APIを使えるように設定する。<br>

### cronで定期処理
[RaspberryPi3で初めてcrontabを使う前に](https://qiita.com/Higemal/items/5a579b2701ef7c473062)を参照してcronを有効化し、run.shを定期実行するよう設定する。<br>

## 参考書籍
- 「Raspberry Pi クックブック 第2版」Simon Monk著 水原 文訳 株式会社オライリー・ジャパン [ISBN978-4-87311-811-6](https://www.oreilly.co.jp/books/9784873118116/)

## 参考サイト
- 「SERVO MOTOR SG90 DATA SHEET」http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf
- 「Raspberry Piカメラモジュールで動画撮影・PCで見られるようにmp4に変換する方法」https://qiita.com/karaage0703/items/48b48680a35936ab83f3
- 「Gmail APIとPythonを使ってメール送信を自動化する方法」https://valmore.work/automate-gmail-sending/
- 「Pythonを使ってGmail APIからメールを取得する」https://qiita.com/orikei/items/73dc1ccc95d1872ab1cf
- 「RaspberryPi3で初めてcrontabを使う前に」https://qiita.com/Higemal/items/5a579b2701ef7c473062

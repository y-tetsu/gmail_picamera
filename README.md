# gmail_picamera
Raspberry Piで作るgmailで操作するPiCamera<br>
![動作例](https://github.com/y-tetsu/gmail_picamera/blob/master/image/circle2.gif)

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

## 動作確認環境
- Raspbian GNU/Linux 9.8 (stretch)
- Python3.5.3
    - picamera
    - RPi.GPIO
    - pigpio

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

※編集中

## 参考書籍
- 「Raspberry Pi クックブック 第2版」Simon Monk著 水原 文訳 株式会社オライリー・ジャパン [ISBN978-4-87311-811-6](https://www.oreilly.co.jp/books/9784873118116/)

## 参考サイト
- 「SERVO MOTOR SG90 DATA SHEET」http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf
- 「Raspberry Piカメラモジュールで動画撮影・PCで見られるようにmp4に変換する方法」https://qiita.com/karaage0703/items/48b48680a35936ab83f3

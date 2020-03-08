# gmail_picamera
Raspberry Piで作るgmailで操作するPiCamera<br>
![動作例](https://github.com/y-tetsu/gmail_picamera/blob/master/image/circle.gif)

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

## 参考情報
- 「SERVO MOTOR SG90 DATA SHEET」http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf

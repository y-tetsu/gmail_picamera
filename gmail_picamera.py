#!/usr/bin/env python3
#==================
# gmail_pycamera
#==================

import os
import json

from devices import CameraMount
from h264tomp4 import h264tomp4


class GmailPiCamera:
    """
    gmail_picamera
    """
    def __init__(self, setting_file=None):
            self.setting = self.load_setting(setting_file)

    def load_setting(self, setting_file):
            """
            loading setting file
            """
            setting = {
                "VIDEO_WIDTH" : 240,
                "VIDEO_HEIGHT" : 320,
                "VIDEO_FILE_NAME" : './video.mp4'
            }

            if setting_file is not None and os.path.isfile(setting_file):
               with open(setting_file) as f:
                  setting = json.load(f)

            return setting

    def pan(self):
        """
        controll picamera for pan
        """
        width = self.setting["VIDEO_WIDTH"]
        height = self.setting["VIDEO_HEIGHT"]
        file_name = self.setting["VIDEO_FILE_NAME"]
        tmp_file_name = './tmp.h264'

        with CameraMount() as camera:
            camera.video_pan(width, height, tmp_file_name)
            camera.center()
            h264tomp4(tmp_file_name, file_name)

    def tilt(self):
        """
        controll picamera for tilt
        """
        width = self.setting["VIDEO_WIDTH"]
        height = self.setting["VIDEO_HEIGHT"]
        file_name = self.setting["VIDEO_FILE_NAME"]
        tmp_file_name = './tmp.h264'

        with CameraMount() as camera:
            camera.video_tilt(width, height, tmp_file_name)
            camera.center()
            h264tomp4(tmp_file_name, file_name)


if __name__ == '__main__':
    gcamera = GmailPiCamera()
    #gcamera.pan()
    gcamera.tilt()

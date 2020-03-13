#!/usr/bin/env python3
#==================
# gmail_pycamera
#==================

import os
import json

from devices import CameraMount
from h264tomp4 import h264tomp4
from gmail import Gmail


class GmailPiCamera:
    """
    gmail_picamera
    """
    def __init__(self, video_setting=None, gmail_setting=None):
        self.vsetting = self._load_video_setting(video_setting)
        self.gsetting = self._load_gmail_setting(gmail_setting)

    def _load_video_setting(self, video_setting):
        """
        loading setting file
        """
        setting = {
            "width" : 240,
            "height" : 320,
            "filename" : './video.mp4'
        }

        if video_setting is not None and os.path.isfile(video_setting):
           with open(video_setting) as f:
              setting = json.load(f)

        return setting

    def _load_gmail_setting(self, gmail_setting):
        """
        loading setting file
        """
        setting = {
            "sender_address": "SENDER_ADDRESS",
            "to_addresses": [
                "TO_ADDRESS1",
                "TO_ADDRESS2"
            ],
            "token_pickle": "TOKEN_PICKLE",
            "credential": "CREDENTIAL",
            "subject": "SUBJECT",
            "message": "MESSAGE"
        }

        if os.path.isfile(gmail_setting):
            with open(gmail_setting) as f:
                setting = json.load(f)

            return setting

    def video(self, motion):
        """
        video pan or tilt
        """
        width, height, fname, tfname = self._get_video_setting()

        with CameraMount() as camera:
            if motion == 'pan':
                camera.video_pan(width, height, tfname)
            elif motion == 'tilt':
                camera.video_tilt(width, height, tfname)
            else:
                pass

            camera.center()
            h264tomp4(tfname, fname)

    def _get_video_setting(self):
        """
        get video setting
        """
        width = self.vsetting["width"]
        height = self.vsetting["height"]
        fname = self.vsetting["filename"]
        tfname = './tmp.h264'

        return (width, height, fname, tfname)

    def send(self, to_index=None):
        """
        send gmail
        """
        if to_index is not None:
            gmail = Gmail(self.gsetting)
            gmail.send(to_index)


if __name__ == '__main__':
    gcamera = GmailPiCamera('./video_setting.json', './gmail_setting.json')
    gcamera.video('pan')
    gcamera.send(0)

#!/usr/bin/env python3
#==================
# gmail_pycamera
#==================

import os
import json
import datetime
import shutil

from devices import CameraMount
from h264tomp4 import h264tomp4
from gmail import Gmail
from command import parse_command


class GmailPiCamera:
    """
    gmail_picamera
    """
    def __init__(self, video_setting=None, gmail_setting=None, command_setting=None):
        self.vsetting = self._load_video_setting(video_setting)
        self.gsetting = self._load_gmail_setting(gmail_setting)
        self.csetting = self._load_command_setting(command_setting)
        self.history_json = './history.json'
        self.history = self._load_history()
        self.fname = './video.mp4'
        self.tfname = './tmp.h264'
        self.video_store = './videos'
        self.now = None

    def _load_video_setting(self, setting_json):
        """
        loading setting file
        """
        setting = {
            "width": 240,
            "height": 320,
            "store": False
        }

        if setting_json is not None and os.path.isfile(setting_json):
           with open(setting_json) as f:
              setting = json.load(f)

        return setting

    def _load_gmail_setting(self, setting_json):
        """
        loading setting file
        """
        setting = {
            "sender_address": "SENDER_ADDRESS",
            "user_addresses": [
                "USER_ADDRESS1",
                "USER_ADDRESS2"
            ],
            "credential": "CREDENTIAL",
            "subject": "SUBJECT",
            "message": "MESSAGE"
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def _load_command_setting(self, setting_json):
        """
        loading setting file
        """
        setting = {
            "execute": "EXECUTE_COMMAND",
            "pan": "PAN_COMMAND",
            "tilt": "TILT_COMMAND"
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def _load_history(self):
        """
        loading history
        """
        setting = {}
        setting_json = self.history_json

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def _save_history(self):
        """
        save history
        """
        setting_json = self.history_json

        with open(setting_json, 'w') as f:
            json.dump(self.history, f)

    def video(self, motion):
        """
        video pan or tilt
        """
        self.now = None
        width, height, store = self._get_video_setting()

        with CameraMount() as camera:
            if motion == 'pan':
                camera.video_pan(width, height, self.tfname)
            elif motion == 'tilt':
                camera.video_tilt(width, height, self.tfname)
            else:
                raise ValueError("Invalid motion value!")

            camera.center()
            h264tomp4(self.tfname, self.fname)

            d = datetime.datetime.today()
            year = d.strftime("%Y")
            month = d.strftime("%m")
            day = d.strftime("%d")
            now = d.strftime("%Y%m%d%H%M%S")

            if self.vsetting["store"] is True:
                if not os.path.isdir(self.video_store):
                    os.mkdir(self.video_store)
                if not os.path.isdir(self.video_store + "/" + year):
                    os.mkdir(self.video_store + "/" + year)
                if not os.path.isdir(self.video_store + "/" + year + "/" + month):
                    os.mkdir(self.video_store + "/" + year + "/" + month)
                shutil.copyfile(self.fname, self.video_store + "/" + year + "/" + month + "/" + now + ".mp4")

            self.now = now

    def _get_video_setting(self):
        """
        get video setting
        """
        width = self.vsetting["width"]
        height = self.vsetting["height"]
        store = self.vsetting["store"]

        return (width, height, store)

    def send(self, to_index=None):
        """
        send gmail
        """
        if self.now is not None:
            gmail = Gmail(self.gsetting)
            gmail.send(to_index, self.fname, self.now + '.mp4')

    def receive(self, from_address=None):
        """
        receive gmail
        """
        gmail = Gmail(self.gsetting)
        date, message = gmail.receive(from_address)

        return date, message

    def parse(self, message=None):
        """
        parse command
        """
        return parse_command(self.csetting, message)


if __name__ == '__main__':
    gcamera = GmailPiCamera('./video_setting.json', './gmail_setting.json', './command_setting.json')

    for index, address in enumerate(gcamera.gsetting['user_addresses']):
        # receive
        date, message = gcamera.receive(address)

        # check history
        if not (address in gcamera.history and date == gcamera.history[address]):
            # save history
            gcamera.history[address] = date
            gcamera._save_history()

            # parse command
            command = gcamera.parse(message)
            print(command)

            # execute command
            if command:
                gcamera.video(command)
                gcamera.send(index)

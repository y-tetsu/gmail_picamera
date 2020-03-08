#!/usr/bin/env python3
#==================
# gmail-controller
#==================

import os
import json


class Gmail:
    """
    gmail-controller
    """
    def __init__(self, setting_json):
        self.setting = self.load_setting(setting_json)

    def load_setting(self, setting_json):
        """
        loading setting file
        """
        setting = {
            "login_name": "LOGIN_NAME",
            "login_pass": "LOGIN_PASSWARD",
            "user_addresses": [
                "USER_ADDRESS1",
                "USER_ADDRESS2"
            ]
        }

        if os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting


if __name__ == '__main__':
    gmail = Gmail('./setting.json')
    print(gmail.setting)

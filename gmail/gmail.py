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
    def __init__(self, setting_file):
        self.setting = self.load_setting(setting_file)

    def load_setting(self, setting_file):
        """
        loading setting file
        """
        setting = {
            "user_addresses": [
                "USER_ADDRESS1",
                "USER_ADDRESS2"
            ]
        }

        if os.path.isfile(setting_file):
            with open(setting_file) as f:
                setting = json.load(f)

        return setting


if __name__ == '__main__':
    import getpass

    gmail = Gmail('./setting.json')
    print(gmail.setting)

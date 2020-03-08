#!/usr/bin/env python3
#==================
# gmail-controller
#==================

import os
import json

import crypt_setting


class Gmail:
    """
    gmail-controller
    """
    def __init__(self, enc_setting, password):
        self.setting = self.load_setting(enc_setting, password)

    def load_setting(self, enc_setting, password):
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

        if os.path.isfile(enc_setting):
            with open(enc_setting, 'rb') as f:
                bintext = crypt_setting.decrypt(f.read(), password)
                setting = json.loads(bintext.decode())

        return setting


if __name__ == '__main__':
    import getpass

    password = getpass.getpass('password > ')
    gmail = Gmail('./enc_setting.json', password)
    print(gmail.setting)

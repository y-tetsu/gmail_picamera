#!/usr/bin/env python3
#==================
# encrypt
#==================

import sys
import getpass
import crypt_setting


if __name__ == '__main__':
    password = getpass.getpass('password > ')
    dec = crypt_setting.decrypt(sys.stdin.buffer.read(), password)
    sys.stdout.buffer.write(dec)

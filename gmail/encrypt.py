#!/usr/bin/env python3
#==================
# encrypt
#==================

import sys
import getpass
import crypt_setting


if __name__ == '__main__':
    password = getpass.getpass('password > ')
    confirm = getpass.getpass('confirm > ')

    if password != confirm:
        print('Passwords do not match.')
        sys.exit(0)

    enc = crypt_setting.encrypt(sys.stdin.buffer.read(), password)
    sys.stdout.buffer.write(enc)

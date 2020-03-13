#!/usr/bin/env python3
#==================
# h264 to mp4
#==================

import subprocess

def h264tomp4(src, dst):
    """
    convert h264 to mp4
    """
    cmd = "MP4Box -fps 30 -add " + src + " -new " + dst
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    h264tomp4('./video.h264', './video.mp4')

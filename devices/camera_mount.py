#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control of Camera Mount using PiCamera V2 and two SG90(for pan and tilt)
"""

import sys
sys.path.append('../')

import time
import math

from devices.picamera_v2 import PiCameraV2
from devices.sg90 import Sg90, Sg90hw

STEP_WAIT = 0.005
SWING_INTERVAL = 0.5


class CameraMount():
    """
    Control of Camera Mount
     --------------------------------------------
     gpiop : GPIO-PIN for pan
     gpiot : GPIO-PIN for tilt
     hwp   : True if using Hardware-PWM for gpiop
     hwt   : True if using Hardware-PWM for gpiot
     --------------------------------------------
    """
    def __init__(self, gpiop=18, gpiot=19, hwp=True, hwt=True):
        self.gpiop = gpiop
        self.gpiot = gpiot
        self.hwp = hwp
        self.hwt = hwt
        self.camera = None
        self.servop = None
        self.servot = None
        self.setup()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.cleanup()

    def setup(self):
        """
        setup Camera Mount
        """
        try:
            self.camera = PiCameraV2()

            if self.hwp:
                self.servop = Sg90hw(self.gpiop)
            else:
                self.servop = Sg90(self.gpiop)

            if self.hwt:
                self.servot = Sg90hw(self.gpiot)
            else:
                self.servot = Sg90(self.gpiot)

        except:
            self.cleanup()

    def cleanup(self):
        """
        cleanup Camera Mount
        """
        if self.camera:
            self.camera.cleanup()
            self.camera = None

        if self.servop:
            self.servop.cleanup()
            self.servop = None

        if self.servot:
            self.servot.cleanup()
            self.servot = None

    def start_video(self, width, height, filename):
        """
        start video recording
        """
        self.camera.start_video(width, height, filename)

    def stop_video(self):
        """
        stop video recording
        """
        self.camera.stop_video()

    def center(self):
        """
        set camera in center
        """
        self.servop.center()
        self.servot.center()

    def position(self, x_angle, y_angle):
        """
        set camera at x,y position
        """
        self.servop.move(-x_angle)
        self.servot.move(-y_angle)

    def video_pan(self, width, height, filename):
        """
        recording video while panning
        """
        self.center()
        self.start_video(width, height, filename)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.center_angle, self.servop.max_angle)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.max_angle, self.servop.min_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.min_angle, self.servop.center_angle)
        time.sleep(SWING_INTERVAL)
        self.stop_video()

    def video_tilt(self, width, height, filename):
        """
        recording video while tilting
        """
        self.center()
        self.start_video(width, height, filename)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.center_angle, self.servot.min_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.min_angle, self.servot.max_angle)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.max_angle, self.servot.center_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.stop_video()

    def rotate(self, servo1, servo2, src_angle, dst_angle, step=1):
        """
        rotate servo1 and fix servo2
        """
        resolution = servo1.resolution
        fix_angle = servo2.center_angle

        start = int(src_angle / resolution)
        end = int(dst_angle / resolution) + 1

        for angle in range(start, end, step):
            servo1.move(angle * resolution)
            servo2.move(fix_angle)
            time.sleep(STEP_WAIT)


if __name__ == '__main__':
    with CameraMount() as camera:
        camera.video_pan(240, 320, './video_pan.h264')
        camera.video_tilt(240, 320, './video_tilt.h264')

        camera.center()
        camera.start_video(240, 320, './video_clockwize.h264')

        for degree in range(360*2, 0, -1):
            x = math.cos(math.radians(degree)) * 80
            y = math.sin(math.radians(degree)) * 80
            camera.position(x, y)
            time.sleep(STEP_WAIT * 2)

        camera.center()
        camera.stop_video()

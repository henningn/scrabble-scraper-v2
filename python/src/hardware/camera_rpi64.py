"""
 This file is part of the scrabble-scraper-v2 distribution
 (https://github.com/scrabscrap/scrabble-scraper-v2)
 Copyright (c) 2022 Rainer Rohloff.

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 3.

 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import atexit
import logging
from concurrent.futures import Future
from threading import Event
from time import sleep

import libcamera  # type: ignore
import numpy as np
from picamera2 import Picamera2  # type: ignore

from config import config
from util import Singleton

Mat = np.ndarray[int, np.dtype[np.generic]]


class CameraRPI64(metaclass=Singleton):  # type: ignore
    """implement a camera with rpi native"""

    def __init__(self, resolution=(config.video_width, config.video_height), framerate=config.video_fps, **kwargs):
        logging.info('### init PiCamera')
        self.frame = []
        self.camera = Picamera2()
        self.config = self.camera.create_still_configuration(main={"format": 'XRGB8888', "size": resolution})
        sleep(1)  # warmup camera
        if config.video_rotade:
            self.config["transform"] = libcamera.Transform(hflip=1, vflip=1)  # self.camera.rotation = 180
        self.camera.configure(self.config)
        self.camera.start()
        self.do_wait = round(1 / framerate, 2)
        self.event = None
        atexit.register(self._atexit)

    def _atexit(self) -> None:
        logging.debug('camera close')
        self.camera.close()

    def read(self) -> Mat:
        """read next picture"""
        return self.frame  # type: ignore

    def update(self, event: Event) -> None:
        """update to next picture on thread event"""
        self.event = event
        while True:
            self.frame = self.camera.capture_array()
            if event.is_set():
                break
            sleep(self.do_wait)
        event.clear()

    def cancel(self) -> None:
        """end of video thread"""
        if self.event is not None:
            self.event.set()

    def done(self, result: Future) -> None:
        """signal end of video thread"""
        logging.info(f'cam done {result}')

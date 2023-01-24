'''
 This file is part of the scrabble-scraper-v2 distribution
 (https://github.com/scrabscrap/scrabble-scraper-v2)
 Copyright (c) 2023 Rainer Rohloff.

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 3.

 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import unittest
from threading import Event
from time import sleep

from threadpool import pool
from timer_thread import RepeatedTimer


class RepeatedTestCase(unittest.TestCase):
    '''Test class for timer_thread.py'''

    def setUp(self) -> None:
        self.counter = 0
        return super().setUp()

    def timer_callback(self):
        self.counter += 1

    def test_repeated_timer(self):
        timer = RepeatedTimer(interval=1, function=self.timer_callback)
        _ = pool.submit(timer.tick, Event())
        sleep(2.5)
        timer.cancel()
        self.assertGreaterEqual(self.counter, 2)

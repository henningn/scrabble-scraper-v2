"""
 This file is part of the scrabble-scraper distribution
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
import logging
import logging.config
import os
import unittest
from time import sleep

from hardware.camera_thread import Camera, CameraEnum

TEST_DIR = os.path.dirname(__file__)

logging.config.fileConfig(fname=os.path.dirname(os.path.abspath(__file__)) + '/test_log.conf',
                          disable_existing_loggers=False)


class ScrabbleGameTestCase(unittest.TestCase):

    def config_setter(self, section: str, option: str, value):
        from config import config

        if value is not None:
            if section not in config.config.sections():
                config.config.add_section(section)
            config.config.set(section, option, str(value))
        else:
            config.config.remove_option(section, option)

    def print_board(self, board: dict) -> str:
        result = '  |'
        for i in range(15):
            result += f'{(i + 1):2d} '
        result += ' | '
        for i in range(15):
            result += f'{(i + 1):2d} '
        result += '\n'
        for row in range(15):
            result += f"{chr(ord('A') + row)} |"
            for col in range(15):
                if (col, row) in board:
                    result += f' {board[(col, row)][0]} '
                else:
                    result += ' . '
            result += ' | '
            for col in range(15):
                result += f' {str(board[(col, row)][1])}' if (col, row) in board else ' . '
            result += ' | \n'
        return result

    def setUp(self):
        self.config_setter('output', 'ftp', False)
        pass

    def test_spiel_12(self):
        from state import State

        self.config_setter('video', 'warp_coordinates', None)
        self.config_setter('board', 'layout', 'custom')
        cam = Camera(useCamera=CameraEnum.FILE)
        cam.stream.formatter = f'{TEST_DIR}/game-12/board-{{:02d}}.png'  # type: ignore
        state = State(cam=cam)
        state.do_reset()
        state.game.nicknames = ('A', 'S')
        state.press_button('RED')  # green begins
        for i in range(1, 21):
            cam.stream.cnt = i  # type: ignore
            if i % 2 == 1:
                state.press_button('GREEN')
            else:
                state.press_button('RED')
            if state.last_submit is not None:
                while not state.last_submit.done():  # type: ignore
                    sleep(0.1)
        self.assertEqual(185, state.game.moves[-1].score[0])
        self.assertEqual(208, state.game.moves[-1].score[1])

    def test_spiel_13(self):
        from state import State

        self.config_setter('video', 'warp_coordinates', None)
        self.config_setter('board', 'layout', 'custom')
        cam = Camera(useCamera=CameraEnum.FILE)
        cam.stream.formatter = f'{TEST_DIR}/game-13/board-{{:02d}}.png'  # type: ignore
        # print(f'formatter {cam.stream.formatter}')  # type: ignore
        state = State(cam=cam)
        state.do_reset()
        state.game.nicknames = ('A', 'B')
        state.press_button('RED')  # green begins
        for i in range(1, 26):
            cam.stream.cnt = i  # type: ignore
            if i % 2 == 1:
                state.press_button('GREEN')
            else:
                state.press_button('RED')
            if state.last_submit is not None:
                while not state.last_submit.done():  # type: ignore
                    sleep(0.1)
            # print(state.game.board_str())
        self.assertEqual(501, state.game.moves[-1].score[0])
        self.assertEqual(421, state.game.moves[-1].score[1])

    def test_spiel_14(self):
        from state import State

        self.config_setter('video', 'warp_coordinates', None)
        self.config_setter('board', 'layout', 'custom')
        cam = Camera(useCamera=CameraEnum.FILE)
        cam.stream.formatter = f'{TEST_DIR}/game-14/board-{{:02d}}.png'  # type: ignore
        # print(f'formatter {cam.stream.formatter}')  # type: ignore
        state = State(cam=cam)
        state.do_reset()
        state.game.nicknames = ('INESSA', 'STEFAN')
        state.press_button('RED')  # green begins
        for i in range(1, 28):
            cam.stream.cnt = i  # type: ignore
            if i % 2 == 1:
                state.press_button('GREEN')
            else:
                state.press_button('RED')
            if state.last_submit is not None:
                while not state.last_submit.done():  # type: ignore
                    sleep(0.1)
        self.assertEqual(425, state.game.moves[-1].score[0])
        self.assertEqual(362, state.game.moves[-1].score[1])

    def test_spiel_15(self):
        from state import State

        self.config_setter('video', 'warp_coordinates', None)
        self.config_setter('board', 'layout', 'custom')
        cam = Camera(useCamera=CameraEnum.FILE)
        cam.stream.formatter = f'{TEST_DIR}/game-15/board-{{:02d}}.png'  # type: ignore
        # print(f'formatter {cam.stream.formatter}')  # type: ignore
        state = State(cam=cam)
        state.do_reset()
        state.game.nicknames = ('JO', 'ST')
        state.press_button('GREEN')  # red begins

        for i in range(1, 15):
            cam.stream.cnt = i  # type: ignore
            if i % 2 == 1:
                state.press_button('RED')
            else:
                state.press_button('GREEN')
            if state.last_submit is not None:
                while not state.last_submit.done():  # type: ignore
                    sleep(0.1)

        state.press_button('PAUSE')
        state.press_button('DOUBT1')
        state.press_button('PAUSE')

        for i in range(16, 18):
            cam.stream.cnt = i  # type: ignore
            if i % 2 == 1:
                state.press_button('GREEN')
            else:
                state.press_button('RED')
            if state.last_submit is not None:
                while not state.last_submit.done():  # type: ignore
                    sleep(0.1)

        state.press_button('PAUSE')
        state.press_button('DOUBT1')
        state.press_button('PAUSE')

        for i in range(19, 31):
            cam.stream.cnt = i  # type: ignore
            if i % 2 == 1:
                state.press_button('RED')
            else:
                state.press_button('GREEN')
            if state.last_submit is not None:
                while not state.last_submit.done():  # type: ignore
                    sleep(0.1)

        self.assertEqual(432, state.game.moves[-1].score[0], 'Spieler 1 Score (JO)')
        self.assertEqual(323, state.game.moves[-1].score[1], 'Spieler 2 Score (ST)')


# unit tests per commandline
if __name__ == '__main__':
    unittest.main()
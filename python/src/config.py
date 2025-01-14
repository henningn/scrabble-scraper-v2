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
import configparser
import json
import logging
import os
from typing import Optional

from util import Singleton


class Config(metaclass=Singleton):  # pylint: disable=R0904 # only access to config properties
    """ access to application configuration """

    def __init__(self, ini_file=None) -> None:
        self.config = configparser.ConfigParser()
        self.reload(ini_file=ini_file, clean=False)

    def reload(self, ini_file=None, clean=True) -> None:
        """ reload configuration from file """
        if clean:
            self.config = configparser.ConfigParser()
        try:
            self.config['path'] = {}
            self.config['path']['src_dir'] = os.path.dirname(__file__) or '.'
            self.ini_path = ini_file if ini_file is not None else f'{self.work_dir}/scrabble.ini'
            logging.info(f'reload {self.ini_path}')
            with open(self.ini_path, 'r', encoding="UTF-8") as config_file:
                self.config.read_file(config_file)
        except IOError as oops:
            logging.error(f'can not read INI-File: error({oops.errno}): {oops.strerror}')

    def save(self) -> None:
        """ save configuration to file """
        with open(self.ini_path, 'w', encoding="UTF-8") as config_file:
            val = self.config['path']['src_dir']
            if val == (os.path.dirname(__file__) or '.'):
                self.config.remove_option('path', 'src_dir')
                self.config.write(config_file)
                self.config['path']['src_dir'] = val
            else:
                self.config.write(config_file)

    def config_as_dict(self) -> dict:
        """ get configuration as dict """
        return {s: dict(self.config.items(s)) for s in self.config.sections()}

    @property
    def src_dir(self) -> str:
        """get src dir"""
        return os.path.abspath(self.config.get('path', 'src_dir', fallback=os.path.dirname(__file__) or '.'))

    @property
    def work_dir(self) -> str:
        """get work dir"""
        return os.path.abspath(self.config.get('path', 'work_dir', fallback=f'{self.src_dir}/../work'))

    @property
    def log_dir(self) -> str:
        """"get logging dir"""
        return os.path.abspath(self.config.get('path', 'log_dir', fallback=f'{self.src_dir}/../work/log'))

    @property
    def web_dir(self) -> str:
        """get web folder"""
        return os.path.abspath(self.config.get('path', 'web_dir', fallback=f'{self.src_dir}/../work/web'))

    @property
    def simulate(self) -> bool:
        """should scrabscrap be simuated"""
        return self.config.getboolean('development', 'simulate', fallback=False)

    @property
    def simulate_path(self) -> str:
        """folder for the simulation pictures"""
        return self.config.get('development', 'simulate_path', fallback=self.work_dir + '/simulate/image-{:d}.jpg')

    @property
    def development_recording(self) -> bool:
        """record images in hires and moves to disk"""
        return self.config.getboolean('development', 'recording', fallback=False)

    @property
    def malus_doubt(self) -> int:
        """malus for wrong doubt"""
        return self.config.getint('scrabble', 'malus_doubt', fallback=10)

    @property
    def max_time(self) -> int:
        """maximum play time"""
        return self.config.getint('scrabble', 'max_time', fallback=1800)

    @property
    def min_time(self) -> int:
        """maximum overtime"""
        return self.config.getint('scrabble', 'min_time', fallback=-300)

    @property
    def doubt_timeout(self) -> int:
        """how long is doubt possible"""
        return self.config.getint('scrabble', 'doubt_timeout', fallback=20)

    @property
    def scrabble_verify_moves(self) -> int:
        """moves to look back for tiles corrections"""
        return self.config.getint('scrabble', 'verify_moves', fallback=3)

    @property
    def show_score(self) -> bool:
        """should the display show current score """
        return self.config.getboolean('scrabble', 'show_score', fallback=False)

    @property
    def output_web(self) -> bool:
        """should the game stored into web folder"""
        return self.config.getboolean('output', 'web', fallback=True)

    @property
    def output_ftp(self) -> bool:
        """should ftp upload used"""
        return self.config.getboolean('output', 'ftp', fallback=False)

    # @property
    # def keyboard(self) -> bool:
    #     """should keyboard used as input device"""
    #     return self.simulate or self.config.getboolean('input', 'keyboard', fallback=False)

    @property
    def video_warp(self) -> bool:
        """should warp performed"""
        return self.config.getboolean('video', 'warp', fallback=True)

    @property
    def video_warp_coordinates(self) -> Optional[list]:
        """stored warp coordinates"""
        warp_coordinates_as_string = self.config.get('video', 'warp_coordinates', fallback=None)
        if warp_coordinates_as_string is None or len(warp_coordinates_as_string) <= 0:
            return None
        return json.loads(warp_coordinates_as_string)

    @property
    def video_width(self) -> int:
        """used image width"""
        return self.config.getint('video', 'width', fallback=992)

    @property
    def video_height(self) -> int:
        """used image height"""
        return self.config.getint('video', 'height', fallback=976)

    @property
    def video_fps(self) -> int:
        """used fps on camera monitoring"""
        return self.config.getint('video', 'fps', fallback=30)

    @property
    def video_rotate(self) -> bool:
        """should the images rotated by 180° """
        return self.config.getboolean('video', 'rotate', fallback=False)

    @property
    def board_layout(self) -> str:
        """which board layout should be used"""
        return self.config.get('board', 'layout', fallback='custom').replace('"', '')

    @property
    def tiles_language(self) -> str:
        """used language for the tiles"""
        # use german language as default
        return self.config.get('tiles', 'language', fallback='de')

    @property
    def tiles_image_path(self) -> str:
        """where to find the images for the tiles"""
        # use builtin path as default
        return self.config.get('tiles', 'image_path', fallback=f'{self.src_dir}/game_board/img/default')

    @property
    def tiles_bag(self) -> dict:
        """how many tiles are in the bag"""
        # use german tiles as default
        bag_as_str = self.config.get(self.tiles_language, 'bag',
                                     fallback='{"A": 5, "B": 2, "C": 2, "D": 4, "E": 15, "F": 2, "G": 3, "H": 4, "I": 6, '
                                     '"J": 1, "K": 2, "L": 3, "M": 4, "N": 9, "O": 3, "P": 1, "Q": 1, "R": 6, "S": 7, '
                                     '"T": 6, "U": 6, "V": 1, "W": 1, "X": 1, "Y": 1, "Z": 1, '
                                     '"\u00c4": 1, "\u00d6": 1, "\u00dc": 1, "_": 2}')
        return json.loads(bag_as_str)

    @property
    def tiles_scores(self) -> dict:
        """"scores for the tiles"""
        # use german tiles as default
        bag_as_str = self.config.get(self.tiles_language, 'scores',
                                     fallback='{"A": 1, "B": 3, "C": 4, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, '
                                     '"J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 2, "P": 3, "Q": 10, "R": 1, "S": 1, '
                                     '"T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "_": 0}')
        return json.loads(bag_as_str)

    @property
    def system_quit(self) -> str:
        """on reboot button: should the app just stop (no reboot)"""
        return self.config.get('system', 'quit', fallback='shutdown').replace('"', '')

    @property
    def system_gitbranch(self) -> str:
        """git tag or branch to use for updates"""
        return self.config.get('system', 'gittag', fallback='main').replace('"', '')

    # @property
    # def motion_detection(self) -> str:
    #     """"which mode for motion detection is used"""
    #     return self.config.get('motion', 'detection', fallback='KNN')

    # @property
    # def motion_learning_rate(self) -> float:
    #     """motion learning rate"""
    #     return self.config.getfloat('motion', 'learningRate', fallback=0.1)

    # @property
    # def motion_wait(self) -> float:
    #     """pause between motion detections"""
    #     return self.config.getfloat('motion', 'wait', fallback=0.3)

    # @property
    # def motion_area(self) -> int:
    #     """minimum size of the motion area"""
    #     return self.config.getint('motion', 'area', fallback=1500)


config = Config()

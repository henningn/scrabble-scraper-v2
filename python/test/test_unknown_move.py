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
import logging
import logging.config
import os
import types
import unittest
from typing import List

from scrabble import InvalidMoveExeption

TEST_DIR = os.path.dirname(__file__)

logging.config.fileConfig(fname=os.path.dirname(os.path.abspath(__file__)) + '/test_log.conf',
                          disable_existing_loggers=False)


# https://stackoverflow.com/questions/326910/running-unit-tests-on-nested-functions


def freeVar(val):
    def nested():
        return val
    return nested.__closure__[0]  # type: ignore


def nested(outer, innerName, **freeVars):
    if isinstance(outer, (types.FunctionType, types.MethodType)):
        outer = outer.__code__  # type: ignore
    for const in outer.co_consts:
        if isinstance(const, types.CodeType) and const.co_name == innerName:
            return types.FunctionType(const, globals(), None, None, tuple(
                freeVar(freeVars[name]) for name in const.co_freevars))


class ScrabbleUnknownMoveTestCase(unittest.TestCase):
    """Test class for some scrabble games"""

    def config_setter(self, section: str, option: str, value):
        """set scrabble config"""
        from config import config

        if value is not None:
            if section not in config.config.sections():
                config.config.add_section(section)
            config.config.set(section, option, str(value))
        else:
            config.config.remove_option(section, option)

    def print_board(self, board: dict, changed: List) -> str:
        """print out scrabble board dictionary"""
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
                    result += f'[{board[(col, row)][0]}]' if (col, row) in changed else f' {board[(col, row)][0]} '
                else:
                    result += ' . '
            result += ' | '
            for col in range(15):
                result += f' {str(board[(col, row)][1])}' if (col, row) in board else ' . '
            result += ' | \n'
        return result

    def setUp(self):
        from processing import clear_last_warp

        clear_last_warp()
        self.config_setter('output', 'ftp', False)
        self.config_setter('output', 'web', False)

    def test_unkown_move_01(self):
        """Test removing wrong blanks"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertFalse(is_vertical, msg='horizontal expected')
        self.assertTupleEqual(coord, (3, 7), msg='wrong coords')
        self.assertEqual(word, 'F_RNS', msg='wrong word - expected FIRNS')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_02(self):
        """Test removing wrong blanks"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
            (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (4, 6), (4, 8), (4, 9), (4, 10)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertTrue(is_vertical, msg='vertical expected')
        self.assertTupleEqual(coord, (4, 6), msg='wrong coords')
        self.assertEqual(word, 'V.TEN', msg='wrong word - expected V.TEN')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_03(self):
        """Test removing wrong blanks with blanks in new word"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('_', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
            (4, 6): ('V', 75), (4, 8): ('_', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (4, 6), (4, 8), (4, 9), (4, 10)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertTrue(is_vertical, msg='vertical expected')
        self.assertTupleEqual(coord, (4, 6), msg='wrong coords')
        self.assertEqual(word, 'V._EN', msg='wrong word - expected V._EN')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_04(self):
        """Test removing wrong blanks connection with blank"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 5): ('V', 75), (4, 6): ('_', 75), (4, 8): ('E', 75), (4, 9): ('N', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
            (4, 5): ('V', 75), (4, 6): ('_', 75), (4, 8): ('E', 75), (4, 9): ('N', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (4, 5), (4, 6), (4, 8), (4, 9)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertTrue(is_vertical, msg='vertical expected')
        self.assertTupleEqual(coord, (4, 5), msg='wrong coords')
        self.assertEqual(word, 'V_.EN', msg='wrong word - expected ._EN')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_05(self):
        """Test removing wrong blanks connection with blank"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 8): ('_', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
            (4, 8): ('_', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (4, 8), (4, 9), (4, 10)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertTrue(is_vertical, msg='vertical expected')
        self.assertTupleEqual(coord, (4, 7), msg='wrong coords')
        self.assertEqual(word, '._EN', msg='wrong word - expected ._EN')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_06(self):
        """Test removing wrong blanks connection with blank"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 5): ('V', 75), (4, 6): ('_', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
            (4, 5): ('V', 75), (4, 6): ('_', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (4, 5), (4, 6)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertTrue(is_vertical, msg='vertical expected')
        self.assertTupleEqual(coord, (4, 5), msg='wrong coords')
        self.assertEqual(word, 'V_.', msg='wrong word - expected V_.')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_07(self):
        """Test removing wrong blanks connection with blank"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (8, 6): ('_', 75), (9, 6): ('_', 75),
                 (8, 7): ('_', 75), (9, 7): ('V', 75)}
        expected_board = {
            (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
            (8, 7): ('_', 75), (9, 7): ('V', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (8, 6), (9, 6),
                   (8, 7), (9, 7)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        is_vertical, coord, word, current_board = _find_word(board, sorted(changes))  # type: ignore
        logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('\n' + self.print_board(current_board, changes))
        self.assertFalse(is_vertical, msg='vertical expected')
        self.assertTupleEqual(coord, (3, 7), msg='wrong coords')
        self.assertEqual(word, '....._V', msg='wrong word - expected ....._V')
        self.assertDictEqual(current_board, expected_board, msg='board not equal to expected board')

    def test_unkown_move_10(self):
        """Test one blank in illegal move"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 6): ('X', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        # expected_board = {(3, 6): ('X', 75),
        #                  (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (3, 6),
                   (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        with self.assertRaises(InvalidMoveExeption, msg='InvalidMoveException expected'):
            is_vertical, coord, word, _ = _find_word(board, sorted(changes))  # type: ignore
            logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('invalid board\n' + self.print_board(board, changes))

    def test_unkown_move_11(self):
        """Test tow blanks in illegal move"""
        from processing import _find_word

        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 6): ('X', 75),
                 (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('_', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        # expected_board = {(3, 6): ('X', 75),
        #                  (3, 7): ('F', 75), (4, 7): ('_', 75), (5, 7): ('_', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        changes = [(0, 0), (0, 1), (0, 2), (0, 3),
                   (1, 0), (1, 1), (1, 2), (1, 3),
                   (2, 0), (2, 1), (2, 2), (2, 3),
                   (2, 4), (2, 5), (2, 6), (2, 7),
                   (3, 6),
                   (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)
                   ]

        logging.debug('\n' + self.print_board(board, []))
        with self.assertRaises(InvalidMoveExeption, msg='InvalidMoveException expected'):
            is_vertical, coord, word, _ = _find_word(board, sorted(changes))  # type: ignore
            logging.debug(f'vertical: {is_vertical}, coord: {coord}, word: {word}')
        logging.debug('invalid board\n' + self.print_board(board, changes))


# unit tests per commandline
if __name__ == '__main__':
    unittest.main()

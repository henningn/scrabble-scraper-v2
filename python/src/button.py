"""
 This file is part of the scrabble-scraper distribution (https://github.com/scrabscrap/scrabble-scraper)
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
from enum import Enum

from gpiozero import Button as GpioButton

from state import State


class ButtonEnum(Enum):

    def __str__(self) -> str:
        return self.name

    GREEN = 16  # GPIO16 - pin 36 - Button green
    YELLOW = 17  # GPI1O7 - pin 11 - Button yellow
    RED = 26  # GPIO26 - pin 37 - Button red

    DOUBT0 = 25  # GPIO25 - pin 22 - Button doubt1
    DOUBT1 = 12  # GPIO12 - pin 32 - Button doubt1

    RESET = 23  # GPIO23 - pin 16 - Button reset
    REBOOT = 18  # GPIO18 - pin 12 - Button reboot
    CONFIG = 24  # GPIO24 - pin 18 - Button config


class Button:

    def __init__(self) -> None:
        atexit.register(self.cleanup_atexit)

    def cleanup_atexit(self) -> None:
        # from gpiozero import Device
        # Device.pin_factory.close()  # type: ignore
        pass

    def button_pressed(self, button: GpioButton) -> None:  # callback
        self.state.press_button(ButtonEnum(button.pin.number).name)  # type: ignore

    def button_released(self, button: GpioButton) -> None:  # callback
        self.state.release_button(ButtonEnum(button.pin.number).name)  # type: ignore

    def start(self, _state: State) -> None:
        self.state = _state
        # create Buttons and configure listener
        for b in ButtonEnum:
            if b in [ButtonEnum.GREEN, ButtonEnum.YELLOW, ButtonEnum.RED, ButtonEnum.DOUBT0, ButtonEnum.DOUBT1]:
                logging.debug(f'Button {b.name}')
                nb = GpioButton(b.value)
                nb.when_pressed = self.button_pressed
                nb.when_released = self.button_released
            else:
                logging.debug(f'when held Button {b.name}')
                nb = GpioButton(b.value)
                nb.hold_time = 3
                nb.when_held = self.button_pressed
                nb.when_released = self.button_released
        self.state.do_ready()

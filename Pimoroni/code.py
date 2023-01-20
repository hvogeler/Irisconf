# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

import board
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

import utils

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
km_orig = [Keycode.ZERO,
                Keycode.ONE,
                Keycode.TWO,
                Keycode.THREE,
                Keycode.FOUR,
                Keycode.FIVE,
                Keycode.SIX,
                Keycode.SEVEN,
                Keycode.EIGHT,
                Keycode.NINE,
                Keycode.A,
                Keycode.B,
                Keycode.C,
                Keycode.D,
                Keycode.E,
                Keycode.F]

km_numpad = [Keycode.ZERO,
                Keycode.ONE,
                Keycode.FOUR,
                Keycode.SEVEN,
                Keycode.PERIOD,
                Keycode.TWO,
                Keycode.FIVE,
                Keycode.EIGHT,
                Keycode.ENTER,
                Keycode.THREE,
                Keycode.SIX,
                Keycode.NINE,
                Keycode.ENTER
             ]

km_strings = ["Opus2nr1!\n",    # 0
              "hvogeler\t",     # 1
              "cafeuser\t",     # 4
              "000146",         # 7
              "ssh abinitio\n", # .
              "cd /home/hvo/idea/internal_utils/docker/setups\ndocker-compose -f act-360-full.yml down -v\n", # 2
              "cd /home/hvo/idea/internal_utils/docker/setups\ndocker-compose -f act-360-full.yml up --build --force-recreate ag mhub kafka runtime\n", # 5
              "git rebase main/n",
              "git status\n",   # Blume
              "glol\n",         # 3
              "mvn clean install -DskipTests\n", # 6
              "tmux\n"            # 9
            ]

km_arrows = [Keycode.PAGE_DOWN,        # 0
                Keycode.PAGE_UP,       # 1
                -1,                    
                -1,
                Keycode.LEFT_ARROW ,   # .
                Keycode.HOME,          # 2
                -1,                    
                -1,
                Keycode.DOWN_ARROW,    # Blume
                Keycode.UP_ARROW,      # 3
                -1,
                -1,
                Keycode.RIGHT_ARROW,   # Blumentopf
                Keycode.END,           # Drei Blaetter
                Keycode.BACKSPACE
             ]

IS_LOCKED = True

# Special keys
MODE_KEY = 15
STRING_MODE = 0

# The colour to set the keys when pressed, yellow.
rgb = (255, 0, 0)
rgb_mode = (200,255,200)
rgb_locked = (70, 0, 0)
rgb_off = (0, 0, 0)

modes = [
         km_strings,
         km_arrows,
         km_numpad
        ]

current_mode: int = 0

def set_current_mode(mode):
    global keymap, current_mode
    current_mode = mode % len(modes)
    keymap = modes[current_mode]

    
keys[utils.get_indicator_led(current_mode)].set_led(*rgb_mode)
keymap = modes[current_mode]
keybow.set_all(*rgb_locked)

lock_buf = []

# Attach handler functions to all of the keys
for key in keys:
    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        global IS_LOCKED, keybow
        global keymap, current_mode
        global lock_buf
        
        if not IS_LOCKED:
            if key.number == MODE_KEY:
                keys[utils.get_indicator_led(current_mode)].led_off()
                set_current_mode(current_mode + 1)
                # keys[utils.get_indicator_led(current_mode)].set_led(*rgb_mode)
                utils.leds_for_mode(keybow, current_mode)
                return
                
            if key.number < len(keymap):
                if current_mode == STRING_MODE:
                    layout.write(keymap[key.number])
                    return
                
                if keymap[key.number] >= 0:
                    keycode = keymap[key.number]
                    keyboard.send(keycode)
                    
        if IS_LOCKED:
            if len(lock_buf) > 4:
                lock_buf = []
                keybow.set_all(*rgb_off)
                keybow.set_all(*rgb_locked)
            else:
                lock_buf.append(key.number)
                if len(lock_buf) == 4:
                    if lock_buf[0] == 0 and \
                       lock_buf[1] == 1 and \
                       lock_buf[2] == 2 and \
                       lock_buf[3] == 10:
                            keybow.set_all(*rgb_off)
                            IS_LOCKED = False
                            lock_buf = []
                            utils.leds_for_mode(keybow, current_mode)
                            #keys[utils.get_indicator_led(current_mode)].set_led(*rgb_mode)
            
    @keybow.on_hold(key)
    def press_hold(key):
        global IS_LOCKED, keybow, current_mode, keymap
        if key.number == MODE_KEY:
            IS_LOCKED = True
            keybow.set_all(*rgb_locked)
            set_current_mode(current_mode - 1)

    # A release handler that turns off the LED
#    @keybow.on_release(key)
#    def release_handler(key):
#        key.led_off()

while True:
    # Always remember to call keybow.update()!
    keybow.update()

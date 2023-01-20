
rgb_mode_selector = (180, 180, 0)
rgb_off = (0, 0, 0)
rgb_arrow = (0, 130, 0)
rgb_pg = (0, 90, 130)
rgb_home_end = (0, 30, 100)
rgb_numpad = (0, 150, 0)
rgb_enter = (0, 80, 120)

MODE_STRING = 0
MODE_ARROW = 1
MODE_NUM_PAD = 2

MODE_STRING_KEYS = [(0, rgb_pg),
                   (1, rgb_pg),
                   (2, rgb_pg),
                   (3, rgb_pg),
                    (4, rgb_arrow),
                   (5, rgb_arrow),
                   (6, rgb_arrow),
                   (7, rgb_arrow),
                   (8, rgb_pg),
                   (9, rgb_pg),
                   (10, rgb_pg),
                   (11, rgb_pg),
                   (12, rgb_arrow),
                   (13, rgb_arrow),
                   (14, rgb_arrow)]

MODE_ARROW_KEYS = [(0, rgb_pg),
                   (1, rgb_pg),
                   (4, rgb_arrow),
                   (5, rgb_home_end),
                   (8, rgb_arrow),
                   (9, rgb_arrow),
                   (12, rgb_arrow),
                   (13, rgb_home_end)]

MODE_NUM_PAD_KEYS = [(0, rgb_numpad),
                   (1, rgb_numpad),
                   (2, rgb_numpad),
                   (3, rgb_numpad),
                    (4, rgb_arrow),
                   (5, rgb_numpad),
                   (6, rgb_numpad),
                   (7, rgb_numpad),
                   (8, rgb_enter),
                   (9, rgb_numpad),
                   (10, rgb_numpad),
                   (11, rgb_numpad),
                   (12, rgb_enter),
                   (13, rgb_off),
                   (14, rgb_off)]

def get_indicator_led(mode: int) -> int:
    return mode * 4

def base_leds(keybow):
    keys = keybow.keys
    keybow.set_all(*rgb_off)
    keys[15].set_led(*rgb_mode_selector)
    
def set_leds(keys, mode_keys):
    for key_rgb in mode_keys:
        keys[key_rgb[0]].set_led(*key_rgb[1])
            
def leds_for_mode(keybow, mode):
    keys = keybow.keys
    base_leds(keybow)
    if mode == MODE_ARROW:
        set_leds(keys, MODE_ARROW_KEYS) 
        return
    if mode == MODE_STRING:
        set_leds(keys, MODE_STRING_KEYS) 
        return
    if mode == MODE_NUM_PAD:
        set_leds(keys, MODE_NUM_PAD_KEYS) 
        return

                 
        
    
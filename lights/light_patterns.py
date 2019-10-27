from light_definitions import MODES

OFF = {'funct': 'off'}
OFF2 = {'funct': 'set_mode', 'm': MODES['Static'], 'r': 0, 'g': 0, 'b': 0}

RESTART = {'funct': 'restart'}
RAINBOW = {'funct': 'set_mode', 'm': MODES["Rainbow"], 's': 128}
RED = {'funct': 'set_mode', 'm': MODES["Static"], 'r': 200}
GREEN = {'funct': 'set_mode', 'm': MODES["Static"], 'g': 200}
BLUE = {'funct': 'set_mode', 'm': MODES["Static"], 'b': 200}
SPARKLE = {'funct': 'set_mode', 'm': MODES["Sparkle"], 's': 128, 'p': 255}

STATIC = {'funct': 'set_mode', 'm': MODES["Static"], 'p': 255}
RUNNING = {'funct': 'set_mode', 'm': MODES["Running Lights"], 's': 166, 'p': 255}
RAINBOW_CYCLE = {'funct': 'set_mode', 'm': MODES["Rainbow Cycle"], 's': 110, 'p': 255}
FIRE_SOFT = {'funct': 'set_mode', 'm': MODES["Fire Flicker (soft)"], 's': 110, 'p': 255}
SINGLE_DYN = {'funct': 'set_mode', 'm': MODES["Single Dynamic"], 's': 0, 'p': 255}
CHASE_RAND = {'funct': 'set_mode', 'm': MODES["Theater Chase Rainbow"], 's': 120, 'p': 255}
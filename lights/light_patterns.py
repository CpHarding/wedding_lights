from light_defs import MODES

OFF = {'funct': 'off'}
RESTART = {'funct': 'restart'}
RAINBOW = {'funct': 'set_mode', 'm': MODES["Rainbow"], 's': 128}
RAINBOW_CYCLE = {'funct': 'set_mode', 'm': MODES["Rainbow Cycle"], 's': 128}
RED = {'funct': 'set_mode', 'm': MODES["Static"], 'r': 200}
GREEN = {'funct': 'set_mode', 'm': MODES["Static"], 'g': 200}
BLUE = {'funct': 'set_mode', 'm': MODES["Static"], 'b': 200}

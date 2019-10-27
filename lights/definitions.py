from light_definitions import MODES
import light_patterns as lp

TABLE1_COL = {'r': 255, 'g': 15, 'b': 67}
TABLE2_COL = {'r': 255, 'g': 242, 'b': 57}
TABLE3_COL = {'r': 15, 'g': 255, 'b': 15}
TABLE4_COL = {'r': 255, 'g': 159, 'b': 15}
TABLE5_COL = {'r': 32, 'g': 91, 'b': 255}
TABLE6_COL = {'r': 255, 'g': 255, 'b': 255}

CONFIG_FILE = 'config.yaml'
DEFAULT_CONFIG = {
    'states': [{'name': 'Entrance',
                'state': {
                    '1': dict(lp.RUNNING, **TABLE1_COL),
                    '2': dict(lp.RUNNING, **TABLE2_COL),
                    '3': dict(lp.RUNNING, **TABLE3_COL),
                    '4': dict(lp.RUNNING, **TABLE4_COL),
                    '5': dict(lp.RUNNING, **TABLE5_COL),
                    '6': dict(lp.RUNNING, **TABLE6_COL),
                    '7': lp.RAINBOW_CYCLE,
                    '8': lp.RAINBOW_CYCLE,
                }},
               {'name': 'Speeches',
                'state': {
                    '1': dict(lp.STATIC, **TABLE1_COL),
                    '2': dict(lp.STATIC, **TABLE2_COL),
                    '3': dict(lp.STATIC, **TABLE3_COL),
                    '4': dict(lp.STATIC, **TABLE4_COL),
                    '5': dict(lp.STATIC, **TABLE5_COL),
                    '6': dict(lp.STATIC, **TABLE6_COL),
                    '7': dict(lp.RAINBOW_CYCLE, **{'s':0}),
                    '8': dict(lp.RAINBOW_CYCLE, **{'s':0}),
                }},
               {'name': 'Food',
                'state': {
                    '1': dict(lp.FIRE_SOFT, **TABLE1_COL),
                    '2': dict(lp.FIRE_SOFT, **TABLE2_COL),
                    '3': dict(lp.FIRE_SOFT, **TABLE3_COL),
                    '4': dict(lp.FIRE_SOFT, **TABLE4_COL),
                    '5': dict(lp.FIRE_SOFT, **TABLE5_COL),
                    '6': dict(lp.FIRE_SOFT, **TABLE6_COL),
                    '7': lp.RAINBOW_CYCLE,
                    '8': lp.RAINBOW_CYCLE,
                }},
               {'name': 'Disco',
                'state': {
                    '1': lp.CHASE_RAND,
                    '2': lp.CHASE_RAND,
                    '3': lp.CHASE_RAND,
                    '4': lp.CHASE_RAND,
                    '5': lp.CHASE_RAND,
                    '6': lp.CHASE_RAND,
                    '7': lp.CHASE_RAND,
                    '8': lp.CHASE_RAND,
                }},
               {'name': 'OFF', 'state': {'all': lp.OFF}},
               ],
    'tables': {
        '1': 'WeddingLight01',
        '2': 'WeddingLight02',
        '3': 'WeddingLight03',
        '4': 'WeddingLight04',
        '5': 'WeddingLight05',
        '6': 'WeddingLight06',
        '7': 'WeddingLight07',
        '8': 'WeddingLight08',
    },
    'buttons': {
        '1': {'name': 'Next State'},
        '2': {'name': 'Prev State'},
        '3': {'name': 'Reset States'},
        '4': {'name': 'OFF', 'state': {'all': lp.OFF}},
        '5': {'name': 'btn_5'},
        '6': {'name': 'All Rainbow', 'state': {'all': lp.RAINBOW}},
        '7': {'name': 'TestLights'},
    },
}

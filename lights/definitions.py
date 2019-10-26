from light_defs import MODES
import light_patterns as lp

CONFIG_FILE = 'config.yaml'
DEFAULT_CONFIG = {
    'states': [{'name': 'mood',
                'state': {
                    '1': lp.RAINBOW,
                    '2': lp.RAINBOW,
                    '3': lp.RAINBOW,
                    '4': lp.RAINBOW,
                    '5': lp.RAINBOW,
                    '6': lp.RAINBOW,
                    '7': lp.RAINBOW,
                    '8': lp.RAINBOW,
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
        '5': {'name': 'RGB',
              'state': {
                  '3': lp.RED,
                  '4': lp.GREEN,
                  '6': lp.BLUE,
              }},
        '6': {'name': 'btn6_name'},
        '7': {'name': 'All Rainbow', 'state': {'all': lp.RAINBOW}},
    },
}

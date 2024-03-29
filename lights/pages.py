import time
import pprint
from flask import redirect, url_for, current_app as ca, render_template, request

import definitions as defs
import light_patterns as lp


def index():
    if ca.data['state_num'] is not None:
        ca.data['state'] = ca.settings['states'][ca.data['state_num']]

    btn_names = [b.get('name') for b in ca.settings['buttons'].values()]
    btn_url = [b.__name__ for b in btn_functs]
    btns = zip(btn_names, btn_url)

    states = [c.get('name') for c in ca.settings['states']]
    clients = [c.replace('Wedding', '') for c in ca.lights.clients]

    return render_template('index.html', btns=btns, data=ca.data, states=states, clients=clients)


def web_config():
    if request.method == 'POST':
        for i in range(1, 8):
            ca.settings['tables'][f'{i}'] = request.form[f'table{i}']
        ca.logger.info(f'Table config: \r\n{pprint.pformat(ca.settings["tables"])}')
    return render_template('config.html', config=ca.settings)


def btn1():
    BTN_NUM = '1'
    if not _run_btn_code(BTN_NUM):
        if ca.data['state_num'] is None:
            ca.data['state_num'] = 0
        elif ca.data['state_num'] < len(ca.settings['states']) - 1:
            ca.data['state_num'] += 1
        ca.lights.decode_state(ca.settings['states'][ca.data['state_num']])
    return redirect(url_for('index'))


def btn2():
    BTN_NUM = '2'
    if not _run_btn_code(BTN_NUM):
        if ca.data['state_num'] > 0:
            ca.data['state_num'] -= 1
        ca.lights.decode_state(ca.settings['states'][ca.data['state_num']])
    return redirect(url_for('index'))


def btn3():
    BTN_NUM = '3'
    if not _run_btn_code(BTN_NUM):
        ca.data['state_num'] = 0
        ca.lights.decode_state(ca.settings['states'][ca.data['state_num']])
    return redirect(url_for('index'))


def btn4():
    BTN_NUM = '4'
    if not _run_btn_code(BTN_NUM):
        pass
    return redirect(url_for('index'))


def btn5():
    BTN_NUM = '5'
    if not _run_btn_code(BTN_NUM):
        pass
    return redirect(url_for('index'))


def btn6():
    BTN_NUM = '6'
    if not _run_btn_code(BTN_NUM):
        pass
    return redirect(url_for('index'))


def btn7():
    BTN_NUM = '7'
    if not _run_btn_code(BTN_NUM):
        ca.lights.set_lights(lp.OFF)
        addrs = []
        for table_num in ca.settings['tables']:
            addr = ca.lights.clients.get(ca.settings['tables'][table_num], False)
            if not addr:
                continue
            addrs.append(addr)
            for color in [lp.RED, lp.GREEN, lp.BLUE]:
                ca.lights.set_lights(color, addr)
                time.sleep(0.5)

        colors = [dict(lp.STATIC, **defs.TABLE1_COL),
                  dict(lp.STATIC, **defs.TABLE2_COL),
                  dict(lp.STATIC, **defs.TABLE3_COL),
                  dict(lp.STATIC, **defs.TABLE4_COL),
                  dict(lp.STATIC, **defs.TABLE5_COL),
                  dict(lp.STATIC, **defs.TABLE6_COL),
                  lp.RAINBOW_CYCLE,
                  lp.RAINBOW_CYCLE,
                  ]
        ca.lights.set_lights(colors, addrs)

    return redirect(url_for('index'))


def _run_btn_code(BTN_NUM):
    """
    Set the data message, and check if this button has override defined in settings.
    :param BTN_NUM: button number
    :return: True if override run, False otherwise
    """
    ca.data['message'] = ca.settings['buttons'].get(BTN_NUM, {}).get('name')

    if ca.settings['buttons'].get(BTN_NUM, {}).get('state'):
        ca.lights.decode_state(ca.settings['buttons'][BTN_NUM]['state'])
        return True
    else:
        return False


# Set up buttons
btn_functs = [btn1, btn2, btn3, btn4, btn5, btn6, btn7]

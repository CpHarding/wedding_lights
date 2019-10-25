import json
import logging
import os

from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect

CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    'states': ['one', 'two', 'three'],
    'tables': {
        1: 'WeddingLight01',
        2: 'WeddingLight02',
        3: 'WeddingLight03',
        4: 'WeddingLight04',
        5: 'WeddingLight05',
        6: 'WeddingLight06',
        7: 'WeddingLight07',
        8: 'WeddingLight08',
    },
}

os.environ['FLASK_ENV'] = 'development'
os.environ['ENV'] = 'development'

app = Flask(__name__, static_folder='assets')
app.logger = logging.getLogger('webapp')
app.data = {
    'message': 'None',
    'state': 'None',
    'state_num': None,
    'config': {},
}


def btn1():
    app.data['message'] = 'btn1'
    if app.data['state_num'] is None:
        app.data['state_num'] = 0
    elif app.data['state_num'] < len(app.data['config']['states']) - 1:
        app.data['state_num'] += 1
    return redirect(url_for('index'))


def btn2():
    app.data['message'] = 'btn2'
    if app.data['state_num'] > 0:
        app.data['state_num'] -= 1
    return redirect(url_for('index'))


def btn3():
    app.data['message'] = 'btn3'
    app.data['state_num'] = 0
    return redirect(url_for('index'))


def btn4():
    app.data['message'] = 'btn4'
    return redirect(url_for('index'))


def btn5():
    app.data['message'] = 'btn5'
    return redirect(url_for('index'))


def btn6():
    app.data['message'] = 'btn6'
    return redirect(url_for('index'))


def btn7():
    app.data['message'] = 'btn7'
    return redirect(url_for('index'))


# Set up buttons
buttons = [btn1, btn2, btn3, btn4, btn5, btn6, btn7]
for funct in buttons:
    app.add_url_rule(f'/{funct.__name__}', funct.__name__, view_func=funct)

names = ['Next', 'Prev', 'Reset', 'Btn4', 'Btn5', 'Btn6', 'Btn7']


@app.route('/')
def index():
    if app.data['state_num'] is not None:
        try:
            app.data['state'] = app.data['config']['states'][app.data['state_num']]
        except IndexError:
            print(f'invalid state num: {app.data["state_num"]}')
    btns = zip(names, [(b.__name__) for b in buttons])
    return render_template('index.html',
                           btns=btns,
                           message=app.data['message'],
                           state=app.data['state'])


@app.route('/web_config', methods=['GET', 'POST'])
def web_config():
    if request.method == 'POST':
        for i in range(1, 8):
            app.data['config']['tables'][i] = request.form[f'table{i}']
        print(app.data['config']['tables'])
    return render_template('config.html', config=app.data['config'])


def load_config():
    try:
        if not os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as f:
                f.write(json.dumps(DEFAULT_CONFIG))
        with open(CONFIG_FILE) as f:
            config = json.loads(f.read())
            app.logger.info(f'loaded config: {config}')
            app.data['config'].update(config)
    except Exception as e:
        app.logger.exception(e)
        return {}


if __name__ == '__main__':
    app.debug = True
    load_config()
    app.run(host='0.0.0.0')

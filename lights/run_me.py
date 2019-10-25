import json
import logging
import os
import pprint

from flask import Flask

import definitions as defs
import log_ext
import pages as pages

os.environ['FLASK_ENV'] = 'development'
os.environ['ENV'] = 'development'

app = Flask(__name__, static_folder='assets')


def setup_webapp():
    """ Sets up the app class with data """
    app.logger = logging.getLogger('WeddingLights.webapp')
    app.data = {
        'message': 'None',
        'state': 'None',
        'state_num': 0,
    }
    app.settings = {}

    app.add_url_rule('/', view_func=pages.index, methods=['GET'])
    app.add_url_rule('/web_config', view_func=pages.web_config, methods=['GET', 'POST'])

    # Add button functions
    for funct in pages.btn_functs:
        app.add_url_rule(f'/{funct.__name__}', funct.__name__, view_func=funct)
    load_config()


def load_config():
    try:
        if not os.path.isfile(defs.CONFIG_FILE):
            with open(defs.CONFIG_FILE, 'w') as f:
                f.write(json.dumps(defs.DEFAULT_CONFIG))
        with open(defs.CONFIG_FILE) as f:
            config = json.loads(f.read())
            app.settings.update(config)
            app.logger.info(f'Current Config: {pprint.pformat(app.settings)}')
    except Exception as e:
        app.logger.exception(e)


if __name__ == '__main__':
    logger = log_ext.setup_logger('WeddingLights')
    logger.setLevel(logging.DEBUG)

    app.debug = True
    setup_webapp()
    app.run(host='0.0.0.0')

import argparse
import json
import logging
import os
import pprint
import yaml

from flask import Flask
from celery import Celery

import definitions as defs
import log_ext
import pages
from async_light_manager import LightManager

os.environ['FLASK_ENV'] = 'development'
os.environ['ENV'] = 'development'

logger = logging.getLogger('WeddingLights')
logger.setLevel(logging.DEBUG)


def create_app(settings):
    """ Sets up the app class with data """
    app = Flask(__name__, static_folder='../assets')

    app.logger = logging.getLogger('WeddingLights.webapp')
    app.logger.info(f'Args: {settings}')
    app.data = {
        'message': 'None',
        'state': 'None',
        'state_num': 0,
    }
    app.settings = {}

    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    app.add_url_rule('/', view_func=pages.index, methods=['GET'])
    app.add_url_rule('/web_config', view_func=pages.web_config, methods=['GET', 'POST'])

    # Add button functions
    for funct in pages.btn_functs:
        app.add_url_rule(f'/{funct.__name__}', funct.__name__, view_func=funct)

    app.settings.update(load_config(app))
    app.logger.debug(f'Current Config: \n{pprint.pformat(app.settings)}')

    app.lights = LightManager({'scan':not settings.get('skip_scan', False),
                               'tables': app.settings['tables']})
    # app.celery = make_celery(app)
    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def load_config(app):
    config = {}
    try:
        if not os.path.isfile(defs.CONFIG_FILE):
            with open(defs.CONFIG_FILE, 'w') as f:
                yaml.dump(defs.DEFAULT_CONFIG, f, Dumper=yaml.Dumper)
        with open(defs.CONFIG_FILE) as f:
            config = yaml.load(f, Loader=yaml.Loader)
    except Exception as e:
        app.logger.exception(e)
    return config


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', default='DEBUG', help='logging level')
    parser.add_argument('--skip_scan', action='store_true', default=False, help='do not scan for clients')
    return parser


if __name__ == '__main__':
    logger = log_ext.setup_logger('WeddingLights')

    args = vars(get_parser().parse_args())

    # Set log level and display
    logger.setLevel(args.get('log', logging.INFO))
    lvl = logging.getLevelName(logger.getEffectiveLevel())
    getattr(logger, lvl.lower())(f'Log Level: {lvl}')

    app = create_app(args)
    app.debug = False
    app.run(host='0.0.0.0')

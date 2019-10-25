import logging
import logging.handlers
import os

try:
    from colorama import Fore, Back, Style, init as _colorama_init

    _colorama_init(autoreset=True)
except ImportError:
    from types import SimpleNamespace

    Style = SimpleNamespace(DIM='', NORMAL='', BRIGHT='', RESET_ALL='')
    Back = Fore = SimpleNamespace(
        BLACK='', RED='', GREEN='', YELLOW='', BLUE='', MAGENTA='', CYAN='', WHITE='', RESET=''
    )

try:
    import yaml
except ImportError:
    yaml = False

CONFIG = {
    'date_fmt': '%Y-%m-%d_%H:%M:%S',
    'format_str': '%(asctime)17s-%(name)-12s-%(levelname)-8s-%(message)s',
    'detailed_format_str': '(%(module)s-%(funcName)s #%(lineno)d)',
    'colors': {
        'TRACE': "Back.WHITE,Fore.BLACK",
        'DEBUG': "Fore.CYAN",
        'INFO': "Fore.GREEN",
        'WARNING': "Fore.YELLOW",
        'ERROR': "Fore.RED",
        'CRITICAL': "Back.RED,Fore.WHITE",
    },
}


def add_trace(level=5):
    def trace(self, message, *args, **kws):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kws)

    logging.Logger.trace = trace
    logging.addLevelName(level, "TRACE")


class CustomFormatter(logging.Formatter):
    def __init__(self, format_str='', datefmt_str='', detailed_format='', **kwargs):
        self.detailed_fmt = detailed_format
        logging.Formatter.__init__(self, format_str, datefmt_str)

    def format(self, record):
        format_orig = self._fmt
        if record.levelno != logging.DEBUG:
            self._fmt = f'{format_orig}  {self.detailed_fmt}'
        result = logging.Formatter.format(self, record)
        self._fmt = format_orig
        return result


class ColourStreamHandler(logging.StreamHandler):
    def __init__(self, colors=CONFIG['colors'], stream=None):
        super().__init__(stream)
        self.colors = colors

    def emit(self, record):
        try:
            color = self.colors.get(record.levelname, "")
            if color:
                color = self.lookup_color(color)
            term = getattr(self, "terminator", r"\n")
            self.stream.write(f'{color}{self.format(record)}{Style.RESET_ALL}{term}')
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:  # pylint: disable=W0702
            self.handleError(record)

    @staticmethod
    def lookup_color(color):
        """ Convert string 'color' to ansi-string"""
        rtn_color = ''
        lookup = {'Fore': Fore, 'Back': Back}
        try:
            color_split = color.split(',')
            for part in [c.strip() for c in color_split]:
                parts = part.split('.')
                rtn_color += lookup[parts[0]].__getattribute__(parts[1])
        except Exception:  # pylint: disable=W0702
            # just don't color on an error
            pass
        return rtn_color


def setup_logger(
        name,
        base_logger=None,
        log_dir='logs',
        cfg_file='log.cfg',
        config=CONFIG,
        trace_logging=True,
        clear_others=False,
        handles=None,
):
    base_logger = base_logger if base_logger else logging.getLogger('')
    handles = handles if handles else []

    if trace_logging:
        add_trace()

    if yaml:
        if os.path.isfile(cfg_file):
            try:
                with open(cfg_file) as f:
                    config = yaml.load(f, Loader=yaml.Loader)
            except yaml.YAMLError:
                pass
        else:
            with open(cfg_file, 'w') as f:
                yaml.dump(config, f, Dumper=yaml.Dumper)
    if clear_others:
        for handler in base_logger.handlers[:]:
            base_logger.removeHandler(handler)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, '{}.log'.format(os.path.basename(name).split('.')[0]))
    file_h = logging.handlers.TimedRotatingFileHandler(log_file, when="W6", backupCount=4, delay=True)
    console_h = ColourStreamHandler()

    formatter = CustomFormatter(**config)
    console_h.setFormatter(formatter)
    file_h.setFormatter(formatter)

    handles.extend([console_h, file_h])

    for handle in handles:
        base_logger.addHandler(handle)

    return logging.getLogger(name)


if __name__ == '__main__':
    logger = setup_logger('testLogger', log_dir='test_logs')
    logger.setLevel(0)
    logger.critical('Critical')
    logger.error('Error')
    logger.warning('Warning')
    logger.info('Info')
    logger.debug('Debug')
    logger.trace('Trace')

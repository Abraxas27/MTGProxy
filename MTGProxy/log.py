import os
import logging
from param import LOG_DIR
import sys

from logging import FileHandler
from logging import StreamHandler
from logging import Filter

FILE_HANDLER_LEVEL = logging.DEBUG
CONSOLE_HANDLER_LEVEL = logging.INFO
LOG_FILE = os.path.join(LOG_DIR, 'activity.log')

open(LOG_FILE, 'w').close()

# http://sametmax.com/ecrire-des-logs-en-python/
# https://stackoverflow.com/questions/1383254/logging-streamhandler-and-standard-streams


class MaxLevelFilter(Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno < self.level

logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler = FileHandler(LOG_FILE, 'w')
# on log à minma les WARN dans le fichier
file_handler.setLevel(min(FILE_HANDLER_LEVEL, logging.WARNING))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stdout_hdlr = StreamHandler(sys.stdout)
# on filtre ce qui est plus bas que WARN (qui est redirigé vers stderr)
lower_than_warning = MaxLevelFilter(logging.WARNING)
stdout_hdlr.addFilter(lower_than_warning)
stdout_hdlr.setLevel(CONSOLE_HANDLER_LEVEL)
logger.addHandler(stdout_hdlr)

stderr_hdlr = StreamHandler(sys.stderr)
# on adapte en fonction du niveau choisi, en prenant WARN au maximum (le reste est redirigé vers stdout)
stderr_hdlr.setLevel(max(CONSOLE_HANDLER_LEVEL, logging.WARNING))
logger.addHandler(stderr_hdlr)

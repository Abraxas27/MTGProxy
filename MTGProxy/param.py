import os
import configparser
import re
import csv


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def ensure_file_exists(file):
    if not os.path.exists(file):
        ensure_directory_exists(os.path.dirname(file))
        open(file, 'w').close()


def get_config_or_default(section, option, default_value, check=None):
    return_value = default_value
    try:
        config_value = config.get(section, option)
        if config_value != '' and (check is None or config_value in check):
            return_value = config_value
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
        pass
    finally:
        return return_value


def get_boolean_or_default(section, option, default_value):
    try:
        config_value = config.getboolean(section, option)
        if isinstance(config_value, bool):
            return config_value
        else:
            return default_value
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
        return default_value


def csv_to_dict(file):
    with open(file, 'r', encoding='utf8') as fd:
        return {rows[0].lower(): rows[1].lower() for rows in csv.reader(fd, delimiter=';')}


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
CONF_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'conf'))

config = configparser.ConfigParser()
config.read(os.path.join(CONF_DIR, 'global.ini'))

EDITION_REGEX = '\d{8}\s*(\w*)\s'

LOG_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'logs'))
ensure_directory_exists(LOG_DIR)

OUTPUT_DIR = os.path.join(ROOT_DIR, get_config_or_default('output', 'output_directory', 'output'))
OUTPUT_PROXY_DIR = os.path.join(OUTPUT_DIR, 'Proxy')
if not os.path.isabs(OUTPUT_DIR):
    OUTPUT_DIR = os.path.realpath(os.path.join(ROOT_DIR, OUTPUT_DIR))
ensure_directory_exists(OUTPUT_PROXY_DIR)

NOT_FOUND_FILE = os.path.join(OUTPUT_DIR, "not_found.txt")

DEFAULT_PROXY_FILE = os.path.join(ROOT_DIR, 'input', 'Proxy.txt')
PROXY_FILE = get_config_or_default('input', 'proxy_list', DEFAULT_PROXY_FILE)
if PROXY_FILE == DEFAULT_PROXY_FILE:
    ensure_file_exists(DEFAULT_PROXY_FILE)

DEFAULT_OUTPUT_FILE_NAME = os.path.basename(PROXY_FILE).split('.')[0]
OUTPUT_TYPE = get_config_or_default('output', 'output_type', 'scribus', ['scribus', 'pdf'])
if OUTPUT_TYPE == 'pdf':
    OUTPUT_FILE_EXTENSION = '.pdf'
else:
    OUTPUT_FILE_EXTENSION = '.sla'
OUTPUT_FILE_NAME = get_config_or_default('output', 'output_name', DEFAULT_OUTPUT_FILE_NAME) + OUTPUT_FILE_EXTENSION

MODE_PRIORITY = get_config_or_default('mode', 'mode_priority', "online").lower()

TRY_OTHER_METHOD = get_boolean_or_default('mode', 'try_other_method', False)

EDITION_FILE = os.path.join(CONF_DIR, "Edition.txt")
EDITION_LINES = []
EDITION_TRIGRAMS = []
with open(EDITION_FILE, 'r', encoding='utf8') as fd:
    reg = re.compile(EDITION_REGEX)
    for line in reversed(fd.readlines()):
        EDITION_LINES.append(line)
        trigram = reg.findall(line)[0]
        if trigram != '' and trigram != 'unrevealed':
            EDITION_TRIGRAMS.append(trigram)

CARDS_DOUBLE_FACED = csv_to_dict(os.path.join(CONF_DIR, "double-faced_cards.csv"))

SCANS_DIR = get_config_or_default('input', 'scans_directory', os.path.join(ROOT_DIR, 'scans'))
if not os.path.isabs(SCANS_DIR):
    SCANS_DIR = os.path.realpath(os.path.join(ROOT_DIR, SCANS_DIR))
if MODE_PRIORITY == "offline" or TRY_OTHER_METHOD is True:
    ensure_directory_exists(SCANS_DIR)

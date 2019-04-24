import json
import logging
import os


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s ")
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger


def load_mapping(path):
    # なかったら空で作成
    if not os.path.exists(path):
        update_mapping(path, dict())

    with open(path) as f:
        mapping = json.load(f)
    return mapping


def update_mapping(path, mapping):
    with open(path, 'w') as f:
        json.dump(mapping, f)

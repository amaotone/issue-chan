import logging
import sys


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s ")
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger
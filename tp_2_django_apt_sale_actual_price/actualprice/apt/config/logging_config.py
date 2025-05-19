import logging
import sys

def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

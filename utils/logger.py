import logging

def get_logger(name=__name__):
    logging.basicConfig(level=logging.ERROR)
    return logging.getLogger(name)

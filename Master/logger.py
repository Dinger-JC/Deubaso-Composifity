import logging
from logging.handlers import RotatingFileHandler



def Log(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    if not log.handlers:
        formatter = logging.Formatter('[%(filename)s] [%(asctime)s] [%(levelname)s] -> %(message)s')
        file_logs = RotatingFileHandler('../Master/logs.log', maxBytes = 10 * 1024 * 1024)
        console_logs = logging.StreamHandler()

        for handler in [file_logs, console_logs]:
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            log.addHandler(handler)

    return log
# Стандартные библиотеки
import os
import logging
from logging.handlers import RotatingFileHandler



def Log(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    if not log.handlers:
        directory = os.path.dirname('../data/logs.log')
        if directory:
            os.makedirs(directory, exist_ok = True)

        formatter = logging.Formatter('[%(filename)s] [%(asctime)s] [%(levelname)s] -> %(message)s')
        file_logs = RotatingFileHandler('../data/logs.log', maxBytes = 32 * 1024 * 1024)
        console_logs = logging.StreamHandler()

        for handler in [file_logs, console_logs]:
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            log.addHandler(handler)

    return log

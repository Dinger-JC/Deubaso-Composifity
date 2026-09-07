# Deubaso Composifity
# Logger

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import sys

# Локальные модули
from config import files
from master import *



def Log():
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    if not log.handlers:
        directory = os.path.dirname(files['logs_log'])
        if directory:
            os.makedirs(directory, exist_ok = True)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] -> %(message)s')
        file = RotatingFileHandler(files['logs_log'], maxBytes = 32 * 1024 * 1024)
        console_logs = logging.StreamHandler()

        for handler in [file, console_logs]:
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            log.addHandler(handler)

    return log

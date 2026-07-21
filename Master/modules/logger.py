# Deubaso Composifity
# Logger

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from master import *



def Log():
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    if not log.handlers:
        path = '../data/logs.log'
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok = True)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] -> %(message)s')
        file_logs = RotatingFileHandler(path, maxBytes = 32 * 1024 * 1024)
        console_logs = logging.StreamHandler()

        for handler in [file_logs, console_logs]:
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            log.addHandler(handler)

    return log

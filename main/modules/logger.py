# Deubaso Composifity
# Logger

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import logging
import os
import time
from datetime import timedelta
from functools import wraps
from logging.handlers import RotatingFileHandler

# Локальные модули
from config import factor, files



class Color_Filter(logging.Filter):
    '''Цветовой фильтр для записи в консоли'''
    colors = {
        'INFO': '\033[90m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[38;5;88m',
        'RESET': '\033[0m'
    }

    def filter(self, record):
        '''Фильтр'''
        record.color = self.colors.get(record.levelname, self.colors['RESET'])
        record.reset = self.colors['RESET']
        return True



def Log():
    '''Логгер'''
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    if not log.handlers:
        directory = os.path.dirname(files['data']['logs'])
        if directory:
            os.makedirs(directory, exist_ok = True)

        formatter_file = logging.Formatter('[%(asctime)s] [%(levelname)s] -> %(message)s')
        formatter_console_logs = logging.Formatter('%(color)s[%(asctime)s] [%(levelname)s] -> %(message)s%(reset)s')

        file = RotatingFileHandler(files['data']['logs'], maxBytes = 32 * factor['MiB'])
        console_logs = logging.StreamHandler()

        file.setLevel(logging.INFO)
        file.setFormatter(formatter_file)
        log.addHandler(file)

        console_logs.setLevel(logging.INFO)
        console_logs.addFilter(Color_Filter())
        console_logs.setFormatter(formatter_console_logs)
        log.addHandler(console_logs)
    return log

def Timer(func):
    '''Время скачивания видео'''
    def Decorator(func):
        @wraps(func)
        def Wrapper(*args, **kwargs):

            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            execution_time = timedelta(seconds = end - start)
            total_seconds = int(execution_time.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = execution_time.microseconds // 1000
            logging.getLogger().info(f'Video download time: {hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}')
            return result
        return Wrapper
    return Decorator(func)

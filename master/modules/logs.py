# Deubaso Composifity
# Logs

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import files
from logger import Log
from presets import *

log = Log()



class LOGS():
    '''Окно логов'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)

        # Отрисовка
        Window(self.window, f'{name} - Logs', 'Logs')

    def _(self):
        '''Логи'''
        ...

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

# Deubaso Composifity
# Info

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import files
from logger import Log
from presets import *

log = Log()



class INFO():
    '''Окно информации'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)

        # Отрисовка
        Window(self.window, f'{name} - Info', 'Info')

    def _(self):
        '''Информация'''
        ...

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

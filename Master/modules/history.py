# Deubaso Composifity
# History

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import border_radius_big, border_radius_small, colors, files, font_big, font_small, font_family, name
from master import *
from presets import *
from logger import *
log = Log()



class HISTORY():
    '''Окно настроек'''
    def __init__(self):
        '''Инициализация'''
        # Основное

        # Отрисовка
        self.window = QMainWindow()
        Window(self.window, f'{name} - History', 'History')

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

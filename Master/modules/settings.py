# Deubaso Composifity
# Settings

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from master import *
from logger import *
log = Log()



class SETTINGS():
    '''Окно настроек'''
    def __init__(self, files, core, name, version, colors, size_window, font_family, font_big, font_small):
        '''Инициализация'''
        # Основное
        self.files = files
        self.core = core
        self.name = name
        self.version = version
        self.colors = colors
        self.size_window = size_window
        self.font_family = font_family
        self.font_big = font_big
        self.font_small = font_small

        # Отрисовка
        self.Window()
        self.Text_Top()
        self.Text_Version()

    def Window(self):
        '''Окно настроек'''
        self.window = QMainWindow()
        self.window.setWindowTitle(f'{self.name} - Settings')
        self.window.setWindowIcon(QIcon(str(self.files['icon_icon'])))
        self.window.setFixedSize(self.size_window[0], self.size_window[1])
        self.window.setStyleSheet(f'''
            QMainWindow {{
                background-color: qlineargradient(
                    spread:pad,
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 {self.colors['main_start']},
                    stop:1 {self.colors['main_end']}
                );
            }}
        ''')

    def Text_Top(self):
        '''Заголовок окна'''
        text_label = QLabel('Settings', self.window)
        text_label.setGeometry(20, 20, 960, 55)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet(f'''
            QLabel {{
                color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.colors['hover_start']},
                    stop:1 {self.colors['hover_end']}
                );

                font-family: '{self.font_family}';
                font-size: 40px;
            }}
        ''')

    def Text_Version(self):
        '''Версия'''
        text_version = QLabel(f'Version: {self.version}', self.window)
        text_version.setGeometry(5, 5, 200, 20)
        text_version.setStyleSheet(f'''
            background: transparent;
            color: {self.colors['sub_text']};
            font-family: '{self.font_family}';
            font-size: {self.font_small}px;
        ''')

    def Show(self):
        '''Показ окна настроек'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

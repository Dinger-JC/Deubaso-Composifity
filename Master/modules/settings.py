# Deubaso Composifity
# Settings

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from core import *



class SETTINGS():
    '''Окно настроек'''
    def __init__(self, core, master_window):
        '''Инициализация'''
        # Основное
        self.core = core
        self.master = master_window
        self.size_window = [400, 300]

        # Отрисовка
        self.Window()
        self.Title()

    def Window(self):
        '''Окно настроек'''
        self.window = QMainWindow()
        self.window.setWindowTitle(f'{self.master.name} - Settings')
        self.window.setWindowIcon(QIcon(str(self.core.files['icon_icon'])))
        self.window.setFixedSize(self.size_window[0], self.size_window[1])
        self.window.setStyleSheet(f'''
            QMainWindow {{
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 {self.master.colors['main_start']}, 
                    stop:1 {self.master.colors['main_end']}
                );
            }}
            QLabel {{
                color: {self.master.colors['text']};
                font-family: {self.master.font_family};
                font-size: 24px;
            }}
        ''')

    def Title(self):
        '''Заголовок окна настроек'''
        self.title = QLabel('Settings', self.window)
        self.title.setGeometry(20, 20, 360, 40)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f'''
            QLabel {{
                color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.master.colors['hover_start']},
                    stop:1 {self.master.colors['hover_end']}
                );

                font-family: '{self.master.font_family}';
                font-size: 28px;
            }}
        ''')

    def Show(self):
        '''Показ окна настроек'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

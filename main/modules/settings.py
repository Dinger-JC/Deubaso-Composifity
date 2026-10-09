# Deubaso Composifity
# Settings

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import os

# Локальные модули
from config import files, settings
from history import HISTORY
from info import INFO
from logger import Log
from logs import LOGS
from presets import *

log = Log()



class SETTINGS():
    '''Окно настроек'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)
        self.info = INFO(self.window)
        self.logs = LOGS(self.window)
        self.history = HISTORY(self.window)

        # Отрисовка
        Window(self.window, f'{name} - Settings', 'Settings')

        self.Block_History()
        self.Block_Folder()

        self.Button_Social(Settings_Layouts.Buttons()['github'])
        self.Button_Social(Settings_Layouts.Buttons()['telegram'])
        self.Button_Social(Settings_Layouts.Buttons()['tiktok'])
        self.Button_Info(Settings_Layouts.Buttons()['info'])
        self.Button_Logs(Settings_Layouts.Buttons()['logs'])
        self.Button_Clear_History(Settings_Layouts.Buttons()['clear_history'])

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def Block_Setting(self, name: str, blocks: dict) -> QFrame:
        '''Блок настройки'''
        # Плашка
        card = QFrame(self.window)
        card.setGeometry(*blocks['geometry'])
        card.setToolTip(blocks['tooltip'])
        card.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['other']['fill']};
                border-radius: {border_radius_small}px;
            }}
            
            QToolTip {{
                background-color: {colors['tooltip']['fill']};
                border: 2px solid {colors['tooltip']['stroke']};
                border-radius: 4px;

                color: {colors['signal']['text']};
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

        # Иконка
        icon = QLabel(card)
        icon.setGeometry(10, 10, size_icon.width(), size_icon.height())
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        icon.setPixmap(QPixmap(str(blocks['icon'])).scaled(
            size_icon,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        icon.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        ''')

        # Левый текст
        text_left = QLabel(name, card)
        text_left.setGeometry(50, 10, 418, size_small)
        text_left.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_left.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;
                
                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
        ''')

        # Перегородка
        block = QFrame(card)
        block.setGeometry(478, 10, 4, size_small)
        block.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['other']['press']};
                border-radius: 2px;
            }}
        ''')
        return card

    def Block_History(self):
        '''Блок истории'''
        card = self.Block_Setting('History', Settings_Layouts.Blocks()['history'])
        size = (20, 20)

        # Правый текст
        text_right = QLabel('Show', card)
        text_right.setGeometry(488, 10, 392, size_small)
        text_right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        text_right.setCursor(Qt.CursorShape.PointingHandCursor)
        text_right.mousePressEvent = lambda event: self.history.Show()
        text_right.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;

                color: {colors['signal']['info']};
                font-size: {font_big}px;
            }}

            QLabel:hover {{
                color: {colors['signal']['text']};
            }}
        ''')

        on = QPoint(34, 5)
        off = QPoint(6, 5)

        def Update_Slider(animate: bool = False):
            '''Состояния'''
            if settings['history'] == 1:
                log.info('History is enabled')

                slider.setStyleSheet(f'''
                    QFrame {{
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:0,
                            stop:0 {colors['download']['start']},
                            stop:1 {colors['download']['end']}
                        );
                        border-radius: {border_radius_big}px;
                    }}
                ''')

                circle.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['signal']['text']};
                        border-radius: {border_radius_small}px;
                    }}
                ''')

                if animate:
                    animation.setStartValue(circle.pos())
                    animation.setEndValue(on)
                    animation.start()

                else:
                    circle.setGeometry(on.x(), on.y(), *size)


            else:
                log.info('History is disabled')

                slider.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['other']['press']};
                        border-radius: {border_radius_big}px;
                    }}
                ''')

                circle.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['signal']['info']};
                        border-radius: {border_radius_small}px;
                    }}
                ''')

                if animate:
                    animation.setStartValue(circle.pos())
                    animation.setEndValue(off)
                    animation.start()

                else:
                    circle.setGeometry(off.x(), off.y(), *size)

        def Toggle():
            '''Перезапись в настройки'''
            new_value = 0 if settings['history'] == 1 else 1
            settings['history'] = new_value

            with open(files['data']['settings'], 'w', encoding = 'utf-8') as file:
                json.dump(settings, file, ensure_ascii = False, indent = 2)

            Update_Slider(True)

        # Ползунок
        slider = QFrame(card)
        slider.setGeometry(890, 10, 60, size_small)
        slider.setCursor(Qt.CursorShape.PointingHandCursor)
        slider.mousePressEvent = lambda event: Toggle()
        slider.setStyleSheet(f'''
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['download']['start']},
                    stop:1 {colors['download']['end']}
                );
                border-radius: {border_radius_big}px;
            }}
        ''')

        # Круг
        circle = QFrame(slider)
        circle.setGeometry(on.x(), on.y(), *size)
        circle.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        circle.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['signal']['text']};
                border-radius: {border_radius_small}px;
            }}
        ''')

        Update_Slider(False)

        # Анимация
        animation = QPropertyAnimation(circle, b'pos')
        animation.setDuration(150)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def Block_Folder(self):
        '''Блок выбора папки для видео'''
        def Choose_Folder():
            '''Выбор папки'''
            current_path = settings['path'].replace('\\', '/')
            new_path = QFileDialog.getExistingDirectory(self.window, 'Choose folder', current_path)

            if new_path:
                settings['path'] = new_path
                log.info(f'Video folder has changed: {new_path}')

                with open(files['data']['settings'], 'w', encoding = 'utf-8') as file:
                    json.dump(settings, file, indent = 2, ensure_ascii = False)
                    text_right.setText(new_path.replace('\\', '/'))

        card = self.Block_Setting('The path of saved videos', Settings_Layouts.Blocks()['folder'])

        # Правый текст
        text_right = QPushButton(settings['path'].replace('\\', '/'), card)
        text_right.setGeometry(488, 10, 462, size_small)
        text_right.setCursor(Qt.CursorShape.PointingHandCursor)
        text_right.clicked.connect(Choose_Folder)
        text_right.setStyleSheet(f'''
            QPushButton {{
                background-color: transparent;
                border: none;

                color: {colors['signal']['info']};
                font-size: {font_big}px;
                text-align: right;
            }}
            
            QPushButton:hover {{
                color: {colors['signal']['text']};
            }}
        ''')

    def Button_Preset(self, button: dict) -> QPushButton:
        '''Кнопка'''
        button_body = QPushButton('', self.window)
        button_body.setGeometry(*button['geometry'])
        button_body.setToolTip(button['tooltip'])
        button_body.setIcon(QIcon(str(button['icon']).replace('\\', '/')))
        button_body.setIconSize(size_icon)
        button_body.setCursor(Qt.CursorShape.PointingHandCursor)
        button_body.setStyleSheet(f'''
            QPushButton {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
            
            QPushButton:hover {{
                background-color: {colors['tooltip']['fill']};
                border-color: {colors['tooltip']['stroke']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['other']['press']};
                border-color: {colors['other']['stroke']};
            }}
            
            QToolTip {{
                background-color: {colors['tooltip']['fill']};
                border: 2px solid {colors['tooltip']['stroke']};
                border-radius: 4px;

                color: {colors['signal']['text']};
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')
        return button_body

    def Button_Social(self, button: dict):
        '''Кнопка с ссылкой'''
        def Link():
            '''Переход по ссылке'''
            QDesktopServices.openUrl(QUrl(button['link']))

        body = self.Button_Preset(button)

        if button.get('link'):
            body.clicked.connect(Link)

    def Button_Info(self, button: dict):
        '''Кнопка информации'''
        body = self.Button_Preset(button)
        body.mousePressEvent = lambda event: self.info.Show()

    def Button_Logs(self, button: dict):
        '''Кнопка логов'''
        body = self.Button_Preset(button)
        body.mousePressEvent = lambda event: self.logs.Show()

    def Button_Clear_History(self, button: dict):
        '''Кнопка очистки истории'''
        def Clear_History():
            '''Переход по ссылке'''
            if os.path.exists(files['data']['history']):
                os.remove(files['data']['history'])
                log.info('History cleared')

        body = self.Button_Preset(button)
        if button.get('command'):
            body.clicked.connect(Clear_History)

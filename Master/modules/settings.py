# Deubaso Composifity
# Settings

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import border_radius_big, border_radius_small, colors, files, font_big, font_small, font_family, name, settings
from master import *
from presets import *
from history import *
from logger import *
log = Log()



class SETTINGS():
    '''Окно настроек'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)
        self.history = HISTORY(self.window)

        # Блоки
        self.blocks = {
            'history': {
                'geometry': [20, 95, 960, 50],
                'icon': files['clock_i'],
                'tooltip': 'Record the link history'
            },
            'folder': {
                'geometry': [20, 165, 960, 50],
                'icon': files['folder_i'],
                'tooltip': 'Path for saving downloaded videos'
            }
        }

        # Нижние кнопки
        self.buttons_lower = {
            'github': {
                'geometry': [929, 529, 52, 52],
                'icon': files['github_i'],
                'tooltip': 'Open GitHub repository',
                'link': 'https://github.com/Dinger-JC/Deubaso-Composifity'
            },
            'telegram': {
                'geometry': [859, 529, 52, 52],
                'icon': files['telegram_i'],
                'tooltip': 'Open Telegram channel',
                'link': 'https://t.me/Jitus_Circus'
            },
            'tiktok': {
                'geometry': [789, 529, 52, 52],
                'icon': files['tiktok_i'],
                'tooltip': 'Open TikTok account',
                'link': 'https://www.tiktok.com/@dinger_jitus_circus'
            }
        }

        # Отрисовка
        Window(self.window, f'{name} - Settings', 'Settings')

        self.Block_History()
        self.Block_Folder()

        self.Button_Lower(self.buttons_lower['github'])
        self.Button_Lower(self.buttons_lower['telegram'])
        self.Button_Lower(self.buttons_lower['tiktok'])

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
                background-color: {colors['fill']};
                border-radius: {border_radius_small}px;
            }}
            
            QToolTip {{
                background-color: {colors['hover_fill']};
                border: 2px solid {colors['hover_stroke']};
                border-radius: 4px;

                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

        # Иконка
        icon = QLabel(card)
        icon.setGeometry(10, 10, 30, 30)
        pixmap = QPixmap(str(blocks['icon']))
        scaled_pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(scaled_pixmap)
        icon.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        ''')

        # Левый текст
        text_left = QLabel(name, card)
        text_left.setGeometry(50, 10, 418, 30)
        text_left.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_left.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;
                
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
        ''')

        # Перегородка
        block = QFrame(card)
        block.setGeometry(478, 10, 4, 30)
        block.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['press']};
                border-radius: 2px;
            }}
        ''')
        return card

    def Block_History(self):
        '''Блок истории'''
        card = self.Block_Setting('History', self.blocks['history'])

        # Правый текст
        text_right = QLabel('Show', card)
        text_right.setGeometry(488, 10, 392, 30)
        text_right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        text_right.setCursor(Qt.CursorShape.PointingHandCursor)
        text_right.mousePressEvent = lambda event: self.history.Show()
        text_right.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;

                color: {colors['info']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}

            QLabel:hover {{
                color: {colors['text']};
            }}
        ''')

        on = QPoint(34, 5)
        off = QPoint(6, 5)

        # Состояния
        def Update_Slider(animate: bool = False):
            if settings['history'] == 1:
                log.info('History is enabled')

                slider.setStyleSheet(f'''
                    QFrame {{
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:0,
                            stop:0 {colors['hover_start']},
                            stop:1 {colors['hover_end']}
                        );
                        border-radius: {border_radius_big}px;
                    }}
                ''')

                circle.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['text']};
                        border-radius: {border_radius_small}px;
                    }}
                ''')

                if animate:
                    animation.setStartValue(circle.pos())
                    animation.setEndValue(on)
                    animation.start()

                else:
                    circle.setGeometry(on.x(), on.y(), 20, 20)


            else:
                log.info('History is disabled')

                slider.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['press']};
                        border-radius: {border_radius_big}px;
                    }}
                ''')

                circle.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['info']};
                        border-radius: {border_radius_small}px;
                    }}
                ''')

                if animate:
                    animation.setStartValue(circle.pos())
                    animation.setEndValue(off)
                    animation.start()

                else:
                    circle.setGeometry(off.x(), off.y(), 20, 20)

        # Перезапись в настройки
        def Toggle():
            new_value = 0 if settings['history'] == 1 else 1
            settings['history'] = new_value

            if hasattr(self, 'settings'):
                settings['history'] = new_value

            with open(files['settings_j'], 'w', encoding = 'utf-8') as file:
                json.dump(settings, file, ensure_ascii = False, indent = 2)

            Update_Slider(True)

        # Ползунок
        slider = QFrame(card)
        slider.setGeometry(890, 10, 60, 30)
        slider.setCursor(Qt.CursorShape.PointingHandCursor)
        slider.mousePressEvent = lambda event: Toggle()
        slider.setStyleSheet(f'''
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['hover_start']},
                    stop:1 {colors['hover_end']}
                );
                border-radius: {border_radius_big}px;
            }}
        ''')

        # Круг
        circle = QFrame(slider)
        circle.setGeometry(on.x(), on.y(), 20, 20)
        circle.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        circle.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['text']};
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
            current_path = settings['path'].replace('\\', '/')
            new_path = QFileDialog.getExistingDirectory(self.window, 'Выберите папку', current_path)

            if new_path:
                settings['path'] = new_path
                log.info(f'Video folder has changed: {new_path}')

                with open(files['settings_j'], 'w', encoding = 'utf-8') as file:
                    json.dump(settings, file, indent = 2, ensure_ascii = False)
                    text_right.setText(new_path.replace('\\', '/'))

        card = self.Block_Setting('The path of saved videos', self.blocks['folder'])

        # Правый текст
        text_right = QPushButton(settings['path'].replace('\\', '/'), card)
        text_right.setGeometry(488, 10, 462, 30)
        text_right.setCursor(Qt.CursorShape.PointingHandCursor)
        text_right.clicked.connect(Choose_Folder)
        text_right.setStyleSheet(f'''
            QPushButton {{
                background-color: transparent;
                border: none;

                color: {colors['info']};
                font-family: '{font_family}';
                font-size: {font_big}px;
                text-align: right;
            }}
            
            QPushButton:hover {{
                color: {colors['text']};
            }}
        ''')

    def Button_Lower(self, links: dict):
        '''Кнопка с ссылкой'''
        def Link():
            QDesktopServices.openUrl(QUrl(links['link']))

        button = QPushButton('', self.window)
        button.setGeometry(*links['geometry'])
        button.setToolTip(links['tooltip'])
        button.setIcon(QIcon(str(links['icon']).replace('\\', '/')))
        button.setIconSize(QSize(30, 30))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(Link)
        button.setStyleSheet(f'''
            QPushButton {{
                background-color: {colors['fill']};
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
            
            QPushButton:hover {{
                background-color: {colors['hover_fill']};
                border-color: {colors['hover_stroke']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['press']};
                border-color: {colors['stroke']};
            }}
            
            QToolTip {{
                background-color: {colors['hover_fill']};
                border: 2px solid {colors['hover_stroke']};
                border-radius: 4px;

                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

# Deubaso Composifity
# Settings

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import border_radius_big, border_radius_small, colors, files, font_big, font_small, font_family, name
from master import *
from presets import *
from logger import *
log = Log()



class SETTINGS():
    '''Окно настроек'''
    def __init__(self, core):
        '''Инициализация'''
        # Основное
        self.core = core

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
                'tooltip': 'The path for saving downloaded videos'
            }
        }

        # Ссылки
        self.links = {
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
        self.window = QMainWindow()
        Window(self.window, f'{name} - Settings', 'Settings')

        self.Block_History()
        self.Block_Folder()

        self.Button_Links(self.links['github'])
        self.Button_Links(self.links['telegram'])
        self.Button_Links(self.links['tiktok'])

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def Block_Setting(self, name: str, description: str, blocks: dict, offset: int = 0):
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
        text_right = QLabel(name, card)
        text_right.setGeometry(50, 10, 500, 30)
        text_right.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_right.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;
                
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
        ''')

        # Правый текст
        text_left = QLabel(description, card)
        text_left.setGeometry(395 + offset, 10, 485, 30)
        text_left.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        text_left.setStyleSheet(f'''
            QLabel {{
                background-color: transparent;
            
                color: {colors['info']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
            
            QLabel:hover {{
                font-style: italic;
            }}
        ''')

    def Block_History(self):
        '''Блок истории'''
        self.Block_Setting('History', 'Show', self.blocks['history'], )

        on = QPoint(34, 5)
        off = QPoint(6, 5)

        # Состояния
        def Update_Toggle(animate: bool = False):
            if self.core.settings['history'] == 1:
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
            new_value = 0 if self.core.settings['history'] == 1 else 1
            self.core.settings['history'] = new_value

            if hasattr(self, 'settings'):
                self.settings['history'] = new_value

            with open(files['settings_j'], 'w', encoding = 'utf-8') as file:
                json.dump(self.core.settings, file, ensure_ascii = False, indent = 2)

            Update_Toggle(True)

        # Ползунок
        slider = QFrame(self.window)
        slider.setGeometry(910, 105, 60, 30)
        slider.mousePressEvent = lambda event: Toggle()
        slider.setCursor(Qt.CursorShape.PointingHandCursor)
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

        Update_Toggle(False)

        # Анимация
        animation = QPropertyAnimation(circle, b'pos')
        animation.setDuration(150)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def Block_Folder(self):
        '''Блок выбора пути для видео'''
        self.Block_Setting('The path of saved videos', self.core.settings['path'].replace('\\', '/'), self.blocks['folder'], 70)

    def Button_Links(self, links: dict):
        '''Кнопка с ссылкой'''
        button = QPushButton('', self.window)
        button.setGeometry(*links['geometry'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setToolTip(links['tooltip'])
        button.setIcon(QIcon(str(links['icon']).replace('\\', '/')))
        button.setIconSize(QSize(30, 30))
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

        def Link():
            QDesktopServices.openUrl(QUrl(links['link']))

        button.clicked.connect(Link)

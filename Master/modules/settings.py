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

        # Описания
        self.tooltips = {
            'history': 'Record the link history.'
        }

        # Отрисовка
        self.window = QMainWindow()
        Window(self.window, f'{name} - Settings')

        self.Block_History()

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def Block_History(self):
        '''История'''
        # Плашка
        card = QFrame(self.window)
        card.setGeometry(20, 95, 960, 50)
        card.setToolTip(self.tooltips['history'])
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

        # Название параметра
        text_history = QLabel('History', self.window)
        text_history.setGeometry(60, 105, 200, 30)
        text_history.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_history.setStyleSheet(f'''
            QLabel {{
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
        ''')

        # Показать историю
        text_show = QLabel('Show', self.window)
        text_show.setGeometry(845, 105, 60, 30)
        text_show.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        text_show.setStyleSheet(f'''
            QLabel {{
                color: {colors['sub_text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
        ''')

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
                        background-color: {colors['info']};
                        border-radius: {border_radius_big}px;
                    }}
                ''')

                circle.setStyleSheet(f'''
                    QFrame {{
                        background-color: {colors['sub_text']};
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

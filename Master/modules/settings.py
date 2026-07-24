# Deubaso Composifity
# Settings

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from master import *
from presets import *
from core import *
from logger import *
log = Log()



class SETTINGS():
    '''Окно настроек'''
    def __init__(self, files, core, name, version, colors, size_window, font_family, font_big, font_small, border_radius_small, border_radius_big):
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
        self.border_radius_small = border_radius_small
        self.border_radius_big = border_radius_big

        # Отрисовка
        self.window = QMainWindow()
        Window(
            self.window, self.size_window,
            f'{self.name} - Settings', 'Settings', self.files['icon_i'],
            self.colors['main_start'], self.colors['main_end'],
            self.colors['hover_start'], self.colors['hover_end'],
            self.colors['sub_text'],
            self.font_family, self.font_small,
            self.version
        )

        self.Block_History()

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def Block_History(self):
        '''История'''
        # Плашка
        card = QWidget(self.window)
        card.setGeometry(20, 95, 960, 50)
        card.setStyleSheet(f'''
            background-color: {self.colors['fill']};
            border-radius: {self.border_radius_small}px;
        ''')

        # Название параметра
        text_history = QLabel('History', self.window)
        text_history.setGeometry(60, 105, 200, 30)
        text_history.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_history.setStyleSheet(f'''
            color: {self.colors['text']};
            font-family: '{self.font_family}';
            font-size: {self.font_big}px;
        ''')

        # Показать историю
        text_show = QLabel('Show', self.window)
        text_show.setGeometry(845, 105, 60, 30)
        text_show.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        text_show.setStyleSheet(f'''
            color: {self.colors['sub_text']};
            font-family: '{self.font_family}';
            font-size: {self.font_big}px;
        ''')

        on = QPoint(34, 5)
        off = QPoint(6, 5)

        # Состояния
        def Update_Toggle(animate: bool = False):
            if self.core.settings['history'] == 1:
                log.info('History is enabled.')

                slider.setStyleSheet(f'''
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 {self.colors['hover_start']},
                        stop:1 {self.colors['hover_end']}
                    );
                    border-radius: {self.border_radius_big}px;
                ''')

                circle.setStyleSheet(f'''
                    background-color: {self.colors['text']};
                    border-radius: {self.border_radius_small}px;
                ''')

                if animate:
                    animation.setStartValue(circle.pos())
                    animation.setEndValue(on)
                    animation.start()
                else:
                    circle.setGeometry(on.x(), on.y(), 20, 20)


            else:
                log.info('History is disabled.')

                slider.setStyleSheet(f'''
                    background-color: {self.colors['info']};
                    border-radius: {self.border_radius_big}px;
                ''')

                circle.setStyleSheet(f'''
                    background-color: {self.colors['sub_text']};
                    border-radius: {self.border_radius_small}px;
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

            with open(self.files['settings_j'], 'w', encoding = 'utf-8') as file:
                json.dump(self.core.settings, file, ensure_ascii = False, indent = 2)

            Update_Toggle(True)

        # Ползунок
        slider = QWidget(self.window)
        slider.setGeometry(910, 105, 60, 30)
        slider.mousePressEvent = lambda event: Toggle()
        slider.setStyleSheet(f'''
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['hover_start']},
                stop:1 {self.colors['hover_end']}
            );
            border-radius: {self.border_radius_big}px;
        ''')

        # Круг
        circle = QWidget(slider)
        circle.setGeometry(on.x(), on.y(), 20, 20)
        circle.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        circle.setStyleSheet(f'''
            background-color: {self.colors['text']};
            border-radius: {self.border_radius_small}px;
        ''')

        Update_Toggle(False)

        # Анимация
        animation = QPropertyAnimation(circle, b'pos')
        animation.setDuration(150)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

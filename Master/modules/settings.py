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
    def __init__(self, files, core, name, version, colors, size_window, font_family, font_big, font_small, border_radius):
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
        self.border_radius = border_radius

        # Отрисовка
        self.Window()
        self.Text_Top()
        self.Text_Version()
        self.Block_History()

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def Window(self):
        '''Окно настроек'''
        self.window = QMainWindow()
        self.window.setWindowTitle(f'{self.name} - Settings')
        self.window.setWindowIcon(QIcon(str(self.files['icon_i'])))
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

########################################################################################################################

    def Block_History(self):
        '''История'''
        card = QWidget(self.window)
        card.setGeometry(20, 95, 960, 50)
        card.setStyleSheet(
            'background-color: rgba(255, 255, 255, 38);'
            f'border-radius: {self.border_radius}px;'
        )

        text = QLabel('History', self.window)
        text.setGeometry(60, 105, 200, 30)
        text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text.setStyleSheet(f'''
            color: {self.colors['text']};
            font-family: '{self.font_family}';
            font-size: {self.font_big}px;
        ''')



    def h(self):
        '''История'''
        self.card = QWidget(self.window)
        self.card.setGeometry(20, 95, 960, 50)
        self.card.setStyleSheet(
            'background-color: rgba(255, 255, 255, 38);'
            f'border-radius: {self.border_radius}px;'
        )

        # Шрифт из параметров
        custom_font = QFont(self.font_family, self.font_small)

        # 2. Текст "History"
        self.lbl_history = QLabel("History", self.window)
        self.lbl_history.setGeometry(60, 105, 200, 30)
        self.lbl_history.setFont(custom_font)
        self.lbl_history.setStyleSheet(f"background: transparent; color: {self.colors['sub_text']};")
        self.lbl_history.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 3. Текст "Show"
        self.lbl_show = QLabel("Show", self.window)
        self.lbl_show.setGeometry(845, 105, 60, 30)
        self.lbl_show.setFont(custom_font)
        self.lbl_show.setStyleSheet(f"background: transparent; color: {self.colors['sub_text']};")
        self.lbl_show.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 4. Корпус ползунка (Off/On body)
        self.toggle_body = QWidget(self.window)
        self.toggle_body.setGeometry(910, 105, 60, 30)

        # Переменная состояния внутри этого же метода (True = ON, False = OFF)
        self.toggle_is_on = True

        # Функция для быстрого обновления стилей корпуса
        def update_toggle_style():
            if self.toggle_is_on:
                self.toggle_body.setStyleSheet("""
                    background: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #02DBAC, stop:1 #6392EA);
                    border-radius: 15px;
                """)
            else:
                self.toggle_body.setStyleSheet("""
                    background-color: #444444;
                    border-radius: 15px;
                """)

        update_toggle_style()

        # 5. Бегунок внутри ползунка (круг)
        self.toggle_thumb = QWidget(self.toggle_body)
        self.toggle_thumb.setStyleSheet(f"background-color: #FFFFFF; border-radius: {self.border_radius}px;")

        # Точки позиций бегунка относительно корпуса (left: 944 -> x=34, left: 910 -> x=6)
        self.pos_on = QPoint(34, 5)
        self.pos_off = QPoint(6, 5)
        self.toggle_thumb.setGeometry(self.pos_on.x(), self.pos_on.y(), 20, 20)

        # Анимация движения бегунка
        self.toggle_anim = QPropertyAnimation(self.toggle_thumb, b"pos")
        self.toggle_anim.setDuration(150)
        self.toggle_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

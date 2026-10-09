# Deubaso Composifity
# Logs

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import re

# Локальные модули
from config import files
from logger import Log
from presets import *

log = Log()



class LOGS():
    '''Окно логов'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)

        # Состояние
        self.filter = 'session'
        self.grid = 0
        self.rows = 0
        self.offset = 0
        self.shown = None

        # Отрисовка
        Window(self.window, f'{name} - Logs', 'Logs')

        self.Card()
        self.Button_All()
        self.Button_Session()

        # Обновление
        timer = QTimer(self.window)
        timer.setInterval(100)
        timer.timeout.connect(self.Update_Logs)
        timer.start()

    def Card(self):
        '''Карточка'''
        self.card = QFrame(self.window)
        self.card.setGeometry(20, 95, length, 416)
        self.card.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
            }}
        ''')

        self.list = QListWidget(self.card)
        self.list.setGeometry(10, 10, length - margin, 406)
        self.list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.list.setStyleSheet(f'''
            QListWidget {{
                background-color: transparent;
                border: none;

                color: {colors['signal']['info']};
                font-size: {font_small}px;
                font-family: {files['content']['font_logs']};
                outline: 0;
            }}

            QListWidget::item {{
                border: none;
                background: transparent;
                padding: 0px 10px;
            }}

            QListWidget QScrollBar:vertical {{
                background: transparent;
                width: 10px;
                margin: 5px 2px;
            }}

            QListWidget QScrollBar::handle:vertical {{
                background: {colors['other']['press']};
                border-radius: 4px;
                min-height: 30px;
            }}

            QListWidget QScrollBar::add-line:vertical,
            QListWidget QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QListWidget QScrollBar::add-page:vertical,
            QListWidget QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        ''')

    def Button_All(self):
        '''Кнопка всех логов'''
        self.button_all = QPushButton('All', self.window)
        self.button_all.setGeometry(margin, bottom, 470, size_big)
        self.button_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_all.clicked.connect(lambda: self.Set_Filter('all'))

    def Button_Session(self):
        '''Кнопка текущей сессии'''
        self.button_session = QPushButton('Session', self.window)
        self.button_session.setGeometry(510, bottom, 470, size_big)
        self.button_session.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_session.clicked.connect(lambda: self.Set_Filter('session'))

        self.Update_Buttons()

    def Update_Buttons(self):
        '''Подсветка активного фильтра'''
        active = f'''
            QPushButton {{
                background: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['download']['start']},
                    stop:1 {colors['download']['end']}
                );
                border: none;
                border-radius: {border_radius_small}px;

                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
        '''

        inactive = f'''
            QPushButton {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['signal']['info']};
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
        '''

        self.button_all.setStyleSheet(active if self.filter == 'all' else inactive)
        self.button_session.setStyleSheet(active if self.filter == 'session' else inactive)

    def Set_Filter(self, filter: str):
        '''Установка фильтра'''
        self.filter = filter
        self.Update_Buttons()
        self.Rebuild()

    def Read_Logs(self) -> list:
        '''Чтение файла логов'''
        try:
            with open(files['data']['logs'], encoding = 'utf-8', errors = 'replace') as file:
                return file.readlines()
        except (FileNotFoundError, OSError):
            return []

    def Session_Start(self, lines: list) -> int:
        '''Начало текущего запуска'''
        for index in range(len(lines) - 1, -1, -1):
            if ' [INFO] -> Start' in lines[index]:
                return index
        return 0

    def Add_Line(self, line: str):
        '''Добавление строки лога'''
        def Color(value: str) -> QColor:
            '''RGBA() -> QColor'''
            value = value.strip()
            if value.startswith('rgba'):
                r, g, b, a = [part.strip() for part in value[5:-1].split(',')]
                return QColor(int(r), int(g), int(b), round(255 * float(a)))
            return QColor(value)

        match = re.match(r'\[(.*?)\] \[(\w+)\] -> (.*)', line.strip())
        if not match:
            return

        time, level, message = match.groups()
        item = QListWidgetItem(f'[{time}] [{level}] -> {message}')
        item.setForeground(QBrush(Color(colors['signal'].get(level.lower(), colors['signal']['info']))))
        item.setSizeHint(QSize(0, size_small))
        self.list.addItem(item)

    def Rebuild(self):
        '''Пересборка списка'''
        lines = self.Read_Logs()
        self.offset = self.Session_Start(lines)
        self.grid = len(lines)

        self.list.clear()
        start = self.offset if self.filter == 'session' else 0
        for line in lines[start:]:
            self.Add_Line(line)

        self.rows = len(lines)
        self.shown = self.filter
        self.list.scrollToBottom()

    def Update_Logs(self):
        '''Обновление логов'''
        if not self.window.isVisible():
            return

        lines = self.Read_Logs()
        if not lines:
            return

        offset = self.Session_Start(lines)
        if offset != self.offset or len(lines) < self.rows or self.shown != self.filter:
            self.Rebuild()

        elif len(lines) > self.rows:
            bottom = self.list.verticalScrollBar().value() >= self.list.verticalScrollBar().maximum() - 4

            for line in lines[self.rows:]:
                self.Add_Line(line)

            self.rows = len(lines)
            self.grid = self.rows

            if bottom:
                self.list.scrollToBottom()

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
        self.Update_Logs()

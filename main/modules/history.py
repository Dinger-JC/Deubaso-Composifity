# Deubaso Composifity
# History

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json

# Локальные модули
from config import files
from logger import Log
from presets import *

log = Log()



class HISTORY():
    '''Окно истории'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)

        # Отрисовка
        Window(self.window, f'{name} - History', 'History')

        self.Tree()

    def Tree(self):
        '''Древо'''
        def Copy_Url(item, column):
            '''Копирование ссылки'''
            url = item.text(1)
            if url and url.startswith('http'):
                clipboard = QGuiApplication.clipboard()
                clipboard.setText(url)

        self.tree = QTreeWidget(self.window)
        self.tree.setGeometry(18, 93, size_window[0] - 36, size_window[1] - 111)
        self.tree.setHeaderLabels(['Date', 'Link'])
        self.tree.headerItem().setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
        self.tree.headerItem().setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
        self.tree.setColumnWidth(0, 220)
        self.tree.itemClicked.connect(Copy_Url)
        self.tree.setStyleSheet(f'''
            QTreeWidget {{
                background-color: transparent;
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['signal']['text']};
                font-size: {font_small}px;
                outline: 0;
                show-decoration-selected: 0;
            }}

            QTreeWidget::item {{
                height: {size_small}px;
                border: none;
                border-radius: {border_radius_small}px;

                padding: 0px 4px;
                outline: none;
            }}

            QTreeWidget::item:focus {{
                border: none;
                outline: none;
            }}

            QTreeWidget::item:hover {{
                background-color: {colors['tooltip']['fill']};
            }}

            QTreeWidget::item:selected {{
                background-color: {colors['other']['press']};

                color: {colors['signal']['info']};
            }}

            QHeaderView {{
                background-color: transparent;
                border: none;
            }}

            QHeaderView::section {{
                height: {size_big}px;
                background-color: {colors['other']['fill']};
                border: none;

                color: {colors['signal']['text']};
                font-size: {font_big}px;
                padding: 0px 10px;
            }}

            QHeaderView::section:first {{
                border-top-left-radius: {border_radius_small}px;
                border-bottom-left-radius: {border_radius_small}px;
            }}

            QHeaderView::section:last {{
                border-top-right-radius: {border_radius_small}px;
                border-bottom-right-radius: {border_radius_small}px;
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

        # Перегородка
        line = QFrame(self.window)
        line.setGeometry(238, 105, 4, size_small)
        line.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['other']['press']};
                border-radius: 2px;
            }}
        ''')

    def Load_History(self):
        '''Обновление истории'''
        self.tree.clear()

        try:
            with open(files['data']['history'], encoding = 'utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        for year in sorted(data.keys(), reverse = True):
            year_item = QTreeWidgetItem(self.tree, [f'🌏 {year}'])

            for month in sorted(data[year].keys(), reverse = True):
                month_item = QTreeWidgetItem(year_item, [f'📅 {month}'])

                for date in sorted(data[year][month].keys(), reverse = True):
                    date_item = QTreeWidgetItem(month_item, [f'📌 {date}'])
                    day = data[year][month][date]

                    for time_str in sorted(day.keys(), reverse = True):
                        url = day[time_str]
                        entry_item = QTreeWidgetItem(date_item, [f'🕒 {time_str}', url])
                        entry_item.setToolTip(1, url)

        self.tree.expandAll()

    def Show(self):
        '''Показ окна'''
        self.Load_History()
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

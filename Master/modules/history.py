# Deubaso Composifity
# History

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import border_radius_big, border_radius_small, colors, files, font_big, font_small, font_family, history, name
from master import *
from presets import *
from logger import *
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
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_small}px;
                outline: 0;
                show-decoration-selected: 0;
            }}

            QTreeWidget::item {{
                height: 30px;
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
                background-color: {colors['hover_fill']};
            }}

            QTreeWidget::item:selected {{
                background-color: {colors['press']};

                color: {colors['info']};
            }}

            QHeaderView {{
                background-color: transparent;
                border: none;
            }}

            QHeaderView::section {{
                height: 50px;
                background-color: {colors['fill']};
                border: none;

                color: {colors['text']};
                font-family: '{font_family}';
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
                background-color: {colors['hover_fill']};
                border: 2px solid {colors['hover_stroke']};
                border-radius: 4px;
                
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

        # Перегородка
        line = QFrame(self.window)
        line.setGeometry(238, 105, 4, 30)
        line.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['press']};
                border-radius: 2px;
            }}
        ''')

    def Load_History(self):
        '''Обновление истории'''
        self.tree.clear()

        for year in sorted(history.keys(), reverse = True):
            year_item = QTreeWidgetItem(self.tree, [f'🌏 {year}'])

            for month in sorted(history[year].keys()):
                month_item = QTreeWidgetItem(year_item, [f'📅 {month}'])

                for date in sorted(history[year][month].keys(), reverse = True):
                    date_item = QTreeWidgetItem(month_item, [f'📌 {date}'])
                    day = history[year][month][date]

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

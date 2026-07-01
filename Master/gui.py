# Parser Deubaso Composifity
# Copyright (c) 2026 Dinger_JC
# Master GUI



# Локальные модули
from core import *



class GUI():
    '''Интерфейс'''
    def __init__(self, core):
        '''Инициализация'''
        self.core = core

        # Основное
        self.version = '2026.07.02.0b'
        self.name: str = 'Deubaso Composifity'
        self.size_window: list = [1000, 600]
        self.size_preview: list = [534, 300]

        # Цвета
        self.colors: dict = {
            'main_start': 'rgb(7, 17, 37)',
            'main_end': 'rgb(34, 42, 65)',
            'text': 'rgb(255, 255, 255)',
            'sub_text': 'rgb(180, 180, 180)',
            'stroke': 'rgba(0, 0, 0, 0)',
            'fill': 'rgba(255, 255, 255, 0.15)',
            'hover_stroke': 'rgb(1, 179, 189)',
            'hover_fill': 'rgba(0, 67, 112, 0.5)',
            'hover_start': 'rgb(99, 146, 234)',
            'hover_end': 'rgb(2, 219, 172)',
            'hover_start_pressed': 'rgba(99, 146, 234, 0.4)',
            'hover_end_pressed': 'rgba(2, 219, 172, 0.4)',
            'warning': 'rgb(227, 88, 111)'
        }

        # Шрифт
        self.font_family = 'GungsuhW33-Regular'
        self.font_size_big: int = 18
        self.font_size_small: int = 14

        # Отрисовка
        self.Window()

        self.Name()
        self.Version()

        self.InputBlock()
        self.title = self.TitleBlock(title = 'Name video')
        self.progress = self.ProgressBarBlock()

        self.status = self.StatusBlock()
        self.site = self.SiteBlock()

        self.speed = self.InfoBlock(x = 574, y = 280, title = 'Speed')
        self.max_speed = self.InfoBlock(x = 716, y = 280, title = 'Max speed')
        self.size = self.InfoBlock(x = 858, y = 280, title = 'Size')
        self.quality = self.InfoBlock(x = 574, y = 380, title = 'Quality')
        self.fps = self.InfoBlock(x = 716, y = 380, title = 'FPS')
        self.duration = self.InfoBlock(x = 858, y = 380, title = 'Duration')

        self.DownloadButton()

        self.PreviewBlock()

    def Window(self):
        '''Главное окно'''
        self.window = QMainWindow()
        self.window.setStyleSheet(f'''
            QMainWindow {{
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 {self.colors['main_start']}, 
                    stop:1 {self.colors['main_end']}
                );
            }}
            QLabel {{
                color: {self.colors['text']};
                font-family: {self.font_family};
                font-size: 24px;
            }}
        ''')
        self.window.setWindowTitle(f'{self.name} - porn content parser!')
        self.window.setWindowIcon(QIcon(self.core.files['icon']))
        self.window.setFixedSize(self.size_window[0], self.size_window[1])

    def Name(self):
        '''Название приложения'''
        self.title = QLabel(self.name, self.window)
        self.title.setGeometry(20, 20, 960, 55)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f'''
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

    def Version(self):
        '''Версия'''
        self.version = QLabel(f'Version: {self.version}', self.window)
        self.version.setGeometry(5, 5, 200, 20)
        self.version.setStyleSheet(f'''
            background: transparent;
            color: {self.colors['sub_text']};
            font-family: '{self.font_family}';
            font-size: {self.font_size_small}px;
        ''')

    def InputBlock(self):
        '''Блок строки ввода'''
        self.input = QLineEdit(self.window)
        self.input.setGeometry(20, 95, 960, 50)
        self.input.setPlaceholderText('Insert the link to the video (Strip2, XGroovy, AnalMedia)')
        self.input.returnPressed.connect(self.Info)
        self.input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: 10px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_big}px;
                
                padding-left: 50px;
                padding-right: 15px;
            }}
            QLineEdit:hover {{
                background-color: {self.colors['hover_fill']};
                border-color: {self.colors['hover_stroke']};
            }}
        ''')

        self.icon = QLabel(self.input)
        self.icon.setGeometry(15, 10, 30, 30)
        self.icon.setPixmap(QPixmap(self.core.files['link']))
        self.icon.setScaledContents(True)

    def TitleBlock(self, title: str):
        '''Блок названия контента'''
        # Иконка Download
        self.icon = QLabel(self.window)
        self.icon.setGeometry(21, 165, 44, 45)
        self.icon.setPixmap(QPixmap(self.core.files['download']))
        self.icon.setScaledContents(True)

        # Название видео
        self.title = QLabel(title, self.window)
        self.title.setGeometry(85, 165, 895, 20)
        self.title.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.title.setStyleSheet(f'''
            color: {self.colors['text']};
            font-family: '{self.font_family}';
            font-size: {self.font_size_big}px;
        ''')

        return self.title

    def StatusBlock(self):
        '''Статус'''
        self.status = QLabel('...', self.window)
        self.status.setGeometry(85, 190, 895, 20)
        self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['sub_text']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_size_small}px; 
                }}
            ''')

        return self.status

    def Status(self, type: str, text: str = ''):
        '''Показ статуса'''
        if type == 'status':
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['sub_text']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_size_small}px; 
                }}
            ''')

        if type == 'warning':
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['warning']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_size_small}px; 
                }}
            ''')

        if text:
            self.status.setText(text)
            self.status.raise_()
            self.status.show()
        else:
            self.status.hide()

    def ProgressBarBlock(self):
        '''Полоса загрузки'''
        # Полоса загрузки
        self.progress_bar = QProgressBar(self.window)
        self.progress_bar.setGeometry(20, 230, 960, 30)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(f'''
            QProgressBar {{
                background-color: {self.colors['fill']};
                border-radius: 15px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_big}px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.colors['hover_start']}, 
                    stop:1 {self.colors['hover_end']}
                );
                border-radius: 15px;
            }}
        ''')

        return self.progress_bar

    def InfoBlock(self, x: int, y: int, title: str, value: str = '-'):
        '''Блок информации'''
        block = QFrame(self.window)
        block.setGeometry(x, y, 122, 80)
        block.setStyleSheet(f'''
            QFrame {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: 10px;
            }}
            QFrame:hover {{
                background-color: {self.colors['hover_fill']};
                border-color: {self.colors['hover_stroke']};
            }}
        ''')

        # Название
        title = QLabel(title, block)
        title.setGeometry(10, 10, 102, 30)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f'''
            background: transparent;
            border: none;
        
            color: {self.colors['text']};
            font-family: '{self.font_family}';
            font-size: {self.font_size_big}px;
        ''')

        # Значение
        value = QLabel(value, block)
        value.setGeometry(10, 40, 102, 30)
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value.setStyleSheet(f'''
            background: transparent;
            border: none;
        
            color: {self.colors['sub_text']};
            font-family: '{self.font_family}';
            font-size: {self.font_size_small}px;
        ''')

        return value

    def SiteBlock(self):
        '''Сайт'''
        self.site = QLabel('', self.window)
        self.site.setGeometry(574, 480, 264, 30)
        self.site.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.site.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['text']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_size_big}px; 
                }}
            ''')
        self.site.hide()

        return self.site

    def Site(self, text: str = ''):
        '''Показ сайта'''
        if text:
            self.site.setText(text)
            self.site.raise_()
            self.site.show()
        else:
            self.site.hide()

    def DownloadButton(self):
        '''Кнопка скачивания видео'''
        self.button = QPushButton('Download', self.window)
        self.button.setGeometry(574, 530, 264, 50)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet(f'''
            QPushButton {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.colors['hover_start']}, 
                    stop:1 {self.colors['hover_end']}
                );
                border: transparent;
                border-radius: 10px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_big}px;
            }}
            QPushButton:pressed {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.colors['hover_start_pressed']}, 
                    stop:1 {self.colors['hover_end_pressed']}
                );
                
                color: {self.colors['sub_text']};
            }}
        ''')

        self.button.clicked.connect(self.Download)

    def PreviewBlock(self):
        '''Блок превью'''
        # Основное окно
        self.preview = QLabel(self.window)
        self.preview.setGeometry(20, 280, self.size_preview[0], self.size_preview[1])
        self.preview.setStyleSheet(f'''
            QLabel {{
                background-color: #000000;
                border-radius: 10px;
            }}
        ''')

        # Отображение превью
        self.image = QLabel(self.preview)
        self.image.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.image.setScaledContents(False)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setStyleSheet('''
            background: transparent;
            border: none;
        ''')

        # Подгон размера
        scaled_pixmap = QPixmap(self.core.files['preview']).scaled(
            QSize(self.size_preview[0], self.size_preview[1]),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled_pixmap)

        # Маска
        mask = QBitmap(QSize(self.size_preview[0], self.size_preview[1]))
        mask.fill(Qt.GlobalColor.color0)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.color1)
        painter.drawRoundedRect(0, 0, self.size_preview[0], self.size_preview[1], 10, 10)
        painter.end()

        self.preview.setMask(mask)

    def UpdatePreview(self, preview_path: str = ''):
        '''Подгрузка нового превью'''
        self.load = QPixmap(preview_path)

        scaled_pixmap = self.load.scaled(
            QSize(self.size_preview[0], self.size_preview[1]),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled_pixmap)

    def Reset(self):
        self.title.setText('Name video')

        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)

        self.speed.setText('-')
        self.max_speed.setText('-')
        self.size.setText('-')

        self.quality.setText('-')
        self.fps.setText('-')
        self.duration.setText('-')

    def Info(self):
        '''Запуск основной логики'''
        self.Reset()
        def Thread(url: str):
            self.core.Data(self.core.Link(url))
            self.core.Preview()
            self.core.MoreInfo()

        url = self.input.text()
        self.input.clear()
        thread = threading.Thread(
            target = Thread,
            args = (url,),
            daemon = True
        )
        thread.start()

    def Download(self):
        '''Скачивание'''
        def Thread():
            self.core.DownloadVideo()

        thread = threading.Thread(
            target = Thread,
            args = (),
            daemon = True
        )
        thread.start()



if __name__ == '__main__':
    try:
        other = QApplication(sys.argv)
        core = Core()
        master = GUI(core = core)
        core.gui = master
        master.window.show()
        sys.exit(other.exec())
    except Exception as error:
        log.error(f'Unexpected error: {error}')

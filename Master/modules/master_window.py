# Parser Deubaso Composifity
# Master window

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from core import *



class MASTER():
    '''Главное окно'''
    def __init__(self, core, version):
        '''Инициализация'''
        # Основное
        self.core = core
        self.name = 'Deubaso Composifity'
        self.version = version
        self.size_window = [1000, 600]
        self.size_preview = [534, 300]

        # Цвета
        self.colors = {
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
            'warning': 'rgb(255, 193, 62)',
            'error': 'rgb(227, 88, 111)'
        }

        # Шрифт
        self.font_family = 'GungsuhW33-Regular'
        self.font_size_big = 18
        self.font_size_small = 14

        # Описания
        self.tooltips = {
            'speed': 'Current real-time video download speed',
            'max_speed': 'Maximum fixed speed',
            'size': 'Total video file size',
            'quality': 'Basic video qualities:'
                '\n4K UHD - 3840x2160 (16:9)'
                '\n2K QHD - 2560x1440 (16:9)'
                '\nFull HD - 1920x1080 (16:9)'
                '\nHD - 1280x720 (16:9)'
                '\nVGA - 640x480 (4:3)'
                '\nnHD - 640x360 (16:9)'
                '\nQVGA - 320x240 (4:3)',
            'fps': 'Video frame rate',
            'duration': 'Total video length'
        }

        # Отрисовка
        self.Window()

        self.Name()
        self.Version()

        self.Input_Block()

        self.title = self.Title_Block('Name video')
        self.status = self.Status_Block()

        self.progress = self.Progress_Bar_Block()

        self.speed = self.Info_Block([573, 279], 'Speed', self.tooltips['speed'])
        self.max_speed = self.Info_Block([715, 279], 'Max speed', self.tooltips['max_speed'])
        self.size = self.Info_Block([857, 279], 'Size', self.tooltips['size'])
        self.quality = self.Info_Block([573, 379], 'Quality', self.tooltips['quality'])
        self.fps = self.Info_Block([715, 379], 'FPS', self.tooltips['fps'])
        self.duration = self.Info_Block([857, 379], 'Duration', self.tooltips['duration'])

        self.Download_Button()
        self.Stop_Button()
        self.Settings_Button()

        self.Preview_Block()

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
        self.window.setWindowIcon(QIcon(str(self.core.files['icon_icon'])))
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

    def Input_Block(self):
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
        self.icon.setPixmap(QPixmap(str(self.core.files['link_icon'])))
        self.icon.setScaledContents(True)

    def Title_Block(self, title: str):
        '''Блок названия контента'''
        # Иконка Download
        self.icon = QLabel(self.window)
        self.icon.setGeometry(21, 165, 44, 45)
        self.icon.setPixmap(QPixmap(str(self.core.files['download_icon'])))
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

    def Status_Block(self):
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
        if type == 'info':
            log.info(text)
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['sub_text']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_size_small}px; 
                }}
            ''')

        elif type == 'warning':
            log.warning(text)
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['warning']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_size_small}px; 
                }}
            ''')

        elif type == 'error':
            log.error(text)
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['error']};
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

    def Progress_Bar_Block(self):
        '''Полоса загрузки'''
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

    def Info_Block(self, position: list, title: str, tooltip: str = '', number: str = '-'):
        '''Блок информации'''
        block = QFrame(self.window)
        block.setGeometry(position[0], position[1], 122 + 2, 80 + 2)
        block.setToolTip(tooltip)
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
            QToolTip {{
                background-color: {self.colors['hover_fill']};
                border: 2px solid {self.colors['hover_stroke']};
                border-radius: 4px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_small}px;
                padding: 2px;
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
        value = QLabel(number, block)
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

    def Download_Button(self):
        '''Кнопка скачивания видео'''
        self.download_button = QPushButton('Download', self.window)
        self.download_button.setGeometry(574, 530, 264, 50)
        self.download_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_button.setToolTip('Download video')
        self.download_button.setStyleSheet(f'''
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
            QToolTip {{
                background-color: {self.colors['hover_fill']};
                border: 2px solid {self.colors['hover_stroke']};
                border-radius: 4px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_small}px;
                padding: 2px;
            }}
        ''')

        self.download_button.clicked.connect(self.Download)

    def Stop_Button(self):
        '''Кнопка остановки скачивания видео'''
        self.stop_button = QPushButton('', self.window)
        self.stop_button.setGeometry(858, 530, 51, 50)
        self.stop_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_button.setToolTip('Abort the download')
        self.stop_button.setToolTip('Stop download')
        self.stop_button.setIcon(QIcon(str(self.core.files['stop_icon']).replace('\\', '/')))
        self.stop_button.setIconSize(QSize(20, 20))
        self.stop_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: 10px;

                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_big}px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['hover_fill']};
                border-color: {self.colors['hover_stroke']};
            }}
            QToolTip {{
                background-color: {self.colors['hover_fill']};
                border: 2px solid {self.colors['hover_stroke']};
                border-radius: 4px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_small}px;
                padding: 2px;
            }}
        ''')

        self.stop_button.clicked.connect(self.core.Stop_Download)

    def Settings_Button(self):
        '''Кнопка настроек'''
        self.settings_button = QPushButton('', self.window)
        self.settings_button.setGeometry(929, 530, 51, 50)
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_button.setToolTip('Settings')
        self.settings_button.setIcon(QIcon(str(self.core.files['settings_icon']).replace('\\', '/')))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: 10px;

                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_big}px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['hover_fill']};
                border-color: {self.colors['hover_stroke']};
            }}
            QToolTip {{
                background-color: {self.colors['hover_fill']};
                border: 2px solid {self.colors['hover_stroke']};
                border-radius: 4px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_size_small}px;
                padding: 2px;
            }}
        ''')

        # self.settings_button.clicked.connect()

    def Preview_Block(self):
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

        # Размытие
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(30)
        self.blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.PerformanceHint)

        # Пустой фон
        self.blur = QLabel(self.preview)
        self.blur.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.blur.setStyleSheet('background: transparent; border: none;')
        self.blur.setGraphicsEffect(self.blur_effect)

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
        scaled_pixmap = QPixmap(str(self.core.files['preview_icon'])).scaled(
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

    def Update_Preview(self, preview_path: str = ''):
        '''Подгрузка нового превью'''
        self.load = QPixmap(preview_path)

        blur_pixmap = self.load.scaled(
            QSize(self.size_preview[0], self.size_preview[1]),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.blur.setPixmap(blur_pixmap)

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
            self.core.Get_Data(self.core.Aliases(url))
            self.core.Get_Info()

            self.speed.setText('-')
            self.max_speed.setText('-')
            self.size.setText('-')

            self.core.Get_Preview()
            self.core.Get_Add_Info()

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
            self.core.Download_Video()

        thread = threading.Thread(
            target = Thread,
            args = (),
            daemon = True
        )
        thread.start()

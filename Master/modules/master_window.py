# Deubaso Composifity
# Master window

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from master import *
from settings import *
from logger import *
log = Log()



class MASTER_WINDOW():
    '''Главное окно'''
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

        self.settings = SETTINGS(files, core, name, version, colors, size_window, font_family, font_big, font_small, border_radius)

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
        self.Text_Top()
        self.Text_Version()

        self.Block_Input()

        self.title = self.Text_Content('Name video')
        self.status = self.Text_Status()

        self.progress = self.Block_Progress_Bar()

        self.speed = self.Block_Info([573, 279], 'Speed', self.tooltips['speed'])
        self.max_speed = self.Block_Info([715, 279], 'Max speed', self.tooltips['max_speed'])
        self.size = self.Block_Info([857, 279], 'Size', self.tooltips['size'])
        self.quality = self.Block_Info([573, 379], 'Quality', self.tooltips['quality'])
        self.fps = self.Block_Info([715, 379], 'FPS', self.tooltips['fps'])
        self.duration = self.Block_Info([857, 379], 'Duration', self.tooltips['duration'])

        self.Button_Download()
        self.Button_Stop()
        self.Button_Settings()

        self.Block_Preview()

    def Window(self):
        '''Главное окно'''
        self.window = QMainWindow()
        self.window.setWindowTitle(f'{self.name} - Porn Parser')
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
        text_top = QLabel(self.name, self.window)
        text_top.setGeometry(20, 20, 960, 55)
        text_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_top.setStyleSheet(f'''
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

    def Block_Input(self):
        '''Блок строки ввода'''
        self.input = QLineEdit(self.window)
        self.input.setGeometry(19, 94, 962, 52)
        self.input.setPlaceholderText('Insert the link to the video (Strip2, XGroovy, AnalMedia)')
        self.input.returnPressed.connect(self.Info)
        self.input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: {self.border_radius}px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_big}px;
                
                padding-left: 50px;
                padding-right: 15px;
            }}
            QLineEdit:hover {{
                background-color: {self.colors['hover_fill']};
                border-color: {self.colors['hover_stroke']};
            }}
        ''')

        icon = QLabel(self.input)
        icon.setGeometry(15, 10, 30, 30)
        icon.setPixmap(QPixmap(str(self.files['link_i'])))
        icon.setScaledContents(True)

    def Text_Content(self, title: str):
        '''Блок названия контента'''
        icon = QLabel(self.window)
        icon.setGeometry(21, 165, 44, 45)
        icon.setPixmap(QPixmap(str(self.files['download_i'])))
        icon.setScaledContents(True)

        text = QLabel(title, self.window)
        text.setGeometry(85, 165, 895, 20)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setStyleSheet(f'''
            color: {self.colors['text']};
            font-family: '{self.font_family}';
            font-size: {self.font_big}px;
        ''')
        return text

    def Text_Status(self):
        '''Статус'''
        self.status = QLabel('...', self.window)
        self.status.setGeometry(85, 190, 895, 20)
        self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['sub_text']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_small}px; 
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
                    font-size: {self.font_small}px; 
                }}
            ''')

        elif type == 'warning':
            log.warning(text)
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['warning']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_small}px; 
                }}
            ''')

        elif type == 'error':
            log.error(text)
            self.status.setStyleSheet(f'''
                QLabel {{
                    color: {self.colors['error']};
                    font-family: '{self.font_family}';
                    font-size: {self.font_small}px; 
                }}
            ''')

        if text:
            self.status.setText(text)
            self.status.raise_()
            self.status.show()

        else:
            self.status.hide()

    def Block_Progress_Bar(self):
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
                font-size: {self.font_big}px;
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

    def Block_Info(self, position: list, title: str, tooltip: str = '', number: str = '-'):
        '''Блок информации'''
        block = QFrame(self.window)
        block.setGeometry(position[0], position[1], 122 + 2, 80 + 2)
        block.setToolTip(tooltip)
        block.setStyleSheet(f'''
            QFrame {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: {self.border_radius}px;
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
                font-size: {self.font_small}px;
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
            font-size: {self.font_big}px;
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
            font-size: {self.font_small}px;
        ''')
        return value

    def Button_Download(self):
        '''Кнопка скачивания видео'''
        download_button = QPushButton('Download', self.window)
        download_button.setGeometry(574, 530, 264, 50)
        download_button.setCursor(Qt.CursorShape.PointingHandCursor)
        download_button.setToolTip('Download video')
        download_button.setStyleSheet(f'''
            QPushButton {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.colors['hover_start']}, 
                    stop:1 {self.colors['hover_end']}
                );
                border: transparent;
                border-radius: {self.border_radius}px;
                
                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_big}px;
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
                font-size: {self.font_small}px;
                padding: 2px;
            }}
        ''')

        download_button.clicked.connect(self.Download)

    def Button_Stop(self):
        '''Кнопка остановки скачивания видео'''
        stop_button = QPushButton('', self.window)
        stop_button.setGeometry(858, 530, 51, 50)
        stop_button.setCursor(Qt.CursorShape.PointingHandCursor)
        stop_button.setToolTip('Abort the download')
        stop_button.setToolTip('Stop download')
        stop_button.setIcon(QIcon(str(self.files['stop_i']).replace('\\', '/')))
        stop_button.setIconSize(QSize(20, 20))
        stop_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: {self.border_radius}px;

                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_big}px;
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
                font-size: {self.font_small}px;
                padding: 2px;
            }}
        ''')

        stop_button.clicked.connect(self.core.Stop_Download)

    def Button_Settings(self):
        '''Кнопка настроек'''
        settings_button = QPushButton('', self.window)
        settings_button.setGeometry(929, 530, 51, 50)
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_button.setToolTip('Settings')
        settings_button.setIcon(QIcon(str(self.files['settings_i']).replace('\\', '/')))
        settings_button.setIconSize(QSize(20, 20))
        settings_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.colors['fill']};
                border: 2px solid {self.colors['stroke']};
                border-radius: {self.border_radius}px;

                color: {self.colors['text']};
                font-family: '{self.font_family}';
                font-size: {self.font_big}px;
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
                font-size: {self.font_small}px;
                padding: 2px;
            }}
        ''')

        settings_button.clicked.connect(lambda: self.settings.Show())

    def Block_Preview(self):
        '''Блок превью'''
        self.size_preview = [534, 300]

        # Основное окно
        preview = QLabel(self.window)
        preview.setGeometry(20, 280, self.size_preview[0], self.size_preview[1])
        preview.setStyleSheet(f'''
            QLabel {{
                background-color: #000000;
                border-radius: {self.border_radius}px;
            }}
        ''')

        # Размытие
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(10)
        self.blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.PerformanceHint)

        # Пустой фон
        self.blur = QLabel(preview)
        self.blur.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.blur.setStyleSheet('background: transparent; border: none;')
        self.blur.setGraphicsEffect(self.blur_effect)

        # Отображение превью
        self.image = QLabel(preview)
        self.image.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.image.setScaledContents(False)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setStyleSheet('''
            background: transparent;
            border: none;
        ''')

        # Подгон размера
        scaled_pixmap = QPixmap(str(self.files['preview_i'])).scaled(
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

        preview.setMask(mask)

    def Update_Preview(self, preview_path: str = ''):
        '''Подгрузка нового превью'''
        load = QPixmap(preview_path)

        blur_pixmap = load.scaled(
            QSize(self.size_preview[0], self.size_preview[1]),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.blur.setPixmap(blur_pixmap)

        scaled_pixmap = load.scaled(
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

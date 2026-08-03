# Deubaso Composifity
# Master window

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import border_radius_big, border_radius_small, colors, files, font_big, font_small, font_family, name
from master import *
from presets import *
from settings import *
from logger import *
log = Log()



class MASTER_WINDOW():
    '''Главное окно'''
    def __init__(self, core):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow()
        self.core = core
        self.settings = SETTINGS(self.window)
        self.size_preview = [534, 300]

        # Блоки
        self.blocks = {
            'speed': {
                'geometry': [573, 279, 124, 82],
                'title': 'Speed'
            },
            'max_speed': {
                'geometry': [715, 279, 124, 82],
                'title': 'Max speed'
            },
            'size': {
                'geometry': [857, 279, 124, 82],
                'title': 'Size'
            },
            'quality': {
                'geometry': [573, 379, 124, 82],
                'title': 'Quality'
            },
            'fps': {
                'geometry': [715, 379, 124, 82],
                'title': 'FPS'
            },
            'duration': {
                'geometry': [857, 379, 124, 82],
                'title': 'Duration'
            },
        }

        # Отрисовка
        Window(self.window, f'{name} - Porn Parser', name)

        self.Block_Input()

        self.title = self.Text_Content('Hi, enter the link to the video and download it!')
        self.status = self.Text_Status()

        self.progress = self.Block_Progress_Bar()

        self.speed = self.Block_Info(self.blocks['speed'])
        self.max_speed = self.Block_Info(self.blocks['max_speed'])
        self.size = self.Block_Info(self.blocks['size'])
        self.quality = self.Block_Info(self.blocks['quality'])
        self.fps = self.Block_Info(self.blocks['fps'])
        self.duration = self.Block_Info(self.blocks['duration'])

        self.Button_Download()
        self.Button_Stop()
        self.Button_Settings()

        self.Block_Preview()

        self.window.show()

    def Block_Input(self):
        '''Блок строки ввода'''
        self.input = QLineEdit(self.window)
        self.input.setGeometry(19, 94, 962, 52)
        self.input.setPlaceholderText('Insert the link to the video (Strip2, XGroovy, AnalMedia)')
        self.input.returnPressed.connect(self.Info)
        self.input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {colors['fill']};
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;
                
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
                
                padding-left: 45px;
                padding-right: {border_radius_big}px;
            }}
            
            QLineEdit:hover {{
                background-color: {colors['hover_fill']};
                border-color: {colors['hover_stroke']};
            }}
        ''')

        icon = QLabel(self.input)
        icon.setGeometry(11, 11, 30, 30)
        icon.setPixmap(QPixmap(str(files['link_i'])))
        icon.setScaledContents(True)

    def Text_Content(self, title: str):
        '''Блок названия контента'''
        # Иконка
        icon = QLabel(self.window)
        icon.setGeometry(21, 165, 44, 45)
        icon.setPixmap(QPixmap(str(files['download_i'])))
        icon.setScaledContents(True)

        # Название
        text = QLabel(title, self.window)
        text.setGeometry(85, 165, 895, 20)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setStyleSheet(f'''
            QLabel {{
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
        ''')
        return text

    def Text_Status(self):
        '''Статус'''
        self.status = QLabel('The download status will be displayed here', self.window)
        self.status.setGeometry(85, 190, 895, 20)
        self.status.setStyleSheet(f'''
                QLabel {{
                    color: {colors['info']};
                    font-family: '{font_family}';
                    font-size: {font_small}px; 
                }}
            ''')
        return self.status

    def Status(self, type: str, text: str = ''):
        '''Показ статуса'''
        if type == 'info':
            log.info(text)

        elif type == 'good':
            log.info(text)

        elif type == 'warning':
            log.warning(text)

        elif type == 'error':
            log.error(text)

        self.status.setStyleSheet(f'''
            QLabel {{
                color: {colors.get(type)};
                font-family: '{font_family}';
                font-size: {font_small}px; 
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
                background-color: {colors['fill']};
                border-radius: {border_radius_big}px;
                
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['hover_start']}, 
                    stop:1 {colors['hover_end']}
                );
                border-radius: {border_radius_big}px;
            }}
        ''')
        return self.progress_bar

    def Block_Info(self, blocks: list, number: str = '-') -> QLabel:
        '''Блок информации'''
        block = QFrame(self.window)
        block.setGeometry(*blocks['geometry'])
        block.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['fill']};
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;
            }}
            
            QFrame:hover {{
                background-color: {colors['hover_fill']};
                border-color: {colors['hover_stroke']};
            }}
        ''')

        # Название
        title = QLabel(blocks['title'], block)
        title.setGeometry(10, 10, 102, 30)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;
            
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
        ''')

        # Значение
        value = QLabel(number, block)
        value.setGeometry(10, 40, 102, 30)
        value.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        value.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;
            
                color: {colors['info']};
                font-family: '{font_family}';
                font-size: {font_small}px;
            }}
        ''')
        return value

    def Button_Download(self):
        '''Кнопка скачивания видео'''
        self.button = QPushButton('Download', self.window)
        self.button.setGeometry(574, 530, 264, 50)
        self.button.setToolTip('Download video')
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet(f'''
            QPushButton {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['hover_start']}, 
                    stop:1 {colors['hover_end']}
                );
                border: transparent;
                border-radius: {border_radius_small}px;
                
                color: {colors['text']};
                font-family: '{font_family}';
                font-size: {font_big}px;
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['hover_start_pressed']}, 
                    stop:1 {colors['hover_end_pressed']}
                );
                
                color: {colors['info']};
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

        self.button.clicked.connect(self.Download)
        self.button.setEnabled(False)

    def Button_Stop(self):
        '''Кнопка остановки скачивания видео'''
        button = QPushButton('', self.window)
        button.setGeometry(857, 529, 53, 52)
        button.setToolTip('Abort the download')
        button.setIcon(QIcon(str(files['stop_i']).replace('\\', '/')))
        button.setIconSize(QSize(30, 30))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
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

        button.clicked.connect(self.core.Stop_Download)

    def Button_Settings(self):
        '''Кнопка настроек'''
        button = QPushButton('', self.window)
        button.setGeometry(928, 529, 53, 52)
        button.setToolTip('Settings')
        button.setIcon(QIcon(str(files['settings_i']).replace('\\', '/')))
        button.setIconSize(QSize(30, 30))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
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

        button.clicked.connect(lambda: self.settings.Show())

    def Block_Preview(self):
        '''Блок превью'''
        # Основное окно
        preview = QLabel(self.window)
        preview.setGeometry(20, 280, self.size_preview[0], self.size_preview[1])
        preview.setStyleSheet(f'''
            QLabel {{
                background-color: #000000;
                border-radius: {border_radius_small}px;
            }}
        ''')

        # Размытие
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(10)
        self.blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.PerformanceHint)

        # Пустой фон
        self.blur = QLabel(preview)
        self.blur.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.blur.setGraphicsEffect(self.blur_effect)
        self.blur.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;
            }}
        ''')

        # Отображение превью
        self.image = QLabel(preview)
        self.image.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.image.setScaledContents(False)
        self.image.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;
            }}
        ''')

        # Подгон размера
        scaled_pixmap = QPixmap(str(files['preview_i'])).scaled(
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
        '''Сброс метрик'''
        self.title.setText('Hi, enter the link to the video and download it!')
        self.button.setEnabled(False)

        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)

        self.speed.setText('-')
        self.max_speed.setText('-')
        self.size.setText('-')

        self.quality.setText('-')
        self.fps.setText('-')
        self.duration.setText('-')

    def Info(self):
        '''Поиск основной информации'''
        self.Reset()

        def Thread(url: str):
            self.core.Get_Data(self.core.Aliases(url))
            self.core.Get_Info()

            self.core.Get_Preview()
            self.core.Get_Add_Info()

        url = self.input.text()
        self.input.clear()

        thread = threading.Thread(target = Thread, args = (url,), daemon = True)
        thread.start()

    def Download(self):
        '''Скачивание видео'''
        thread = threading.Thread(target = self.core.Download_Video, daemon = True)
        thread.start()

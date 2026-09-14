# Deubaso Composifity
# Master window

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import math
import threading

# Локальные модули
from config import files
from logger import Log
from presets import *
from settings import SETTINGS

log = Log()


class slow_graph():
    def __call__(self, progress):
        elapsed = progress * 0.6
        frequency = (80 / 1) ** 0.5
        damping_ratio = 20 / (2 * (80 * 1) ** 0.5)
        damped_frequency = frequency * abs(damping_ratio ** 2 - 1) ** 0.5
        decay = math.exp(-damping_ratio * frequency * elapsed)
        if damping_ratio < 1:
            return 1 - decay * (math.cos(damped_frequency * elapsed) + damping_ratio / damped_frequency * math.sin(damped_frequency * elapsed))
        if damping_ratio > 1:
            return 1 - decay * (math.cosh(damped_frequency * elapsed) + damping_ratio / damped_frequency * math.sinh(damped_frequency * elapsed))
        return 1 - decay * (1 + frequency * elapsed)


class MASTER_WINDOW():
    '''Главное окно'''
    def __init__(self, core):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow()
        self.core = core
        self.settings = SETTINGS(self.window)
        self.size_preview = [534, 300]
        self.placeholder = 'Strip2, XGroovy, AnalMedia, Rule34Video'

        # Кнопки
        buttons = {
            'download_video': {
                'geometry': [574, 530, 264, 50],
                'title': 'Download video',
                'tooltip': 'Download video',
                'icon': None
            },
            'stop': {
                'geometry': [857, 529, 53, 52],
                'title': '',
                'tooltip': 'Abort the download',
                'icon': files['images']['png']['buttons']['stop']
            },
            'settings': {
                'geometry': [928, 529, 53, 52],
                'title': '',
                'tooltip': 'Settings',
                'icon': files['images']['png']['buttons']['settings']
            }
        }

        # Блоки
        blocks = {
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

        self.title = self.Text_Content(self.placeholder)
        self.status = self.Text_Status()

        self.Block_Progress_Bar()

        self.speed = self.Block_Info(blocks['speed'])
        self.max_speed = self.Block_Info(blocks['max_speed'])
        self.size = self.Block_Info(blocks['size'])
        self.quality = self.Block_Info(blocks['quality'])
        self.fps = self.Block_Info(blocks['fps'])
        self.duration = self.Block_Info(blocks['duration'])

        self.Button_Download_Video(buttons['download_video'])
        self.Button_Stop(buttons['stop'])
        self.Button_Settings(buttons['settings'])

        self.Block_Preview()

        self.window.show()

    def Block_Input(self):
        '''Блок строки ввода'''
        self.input = QLineEdit(self.window)
        self.input.setGeometry(19, 94, 962, 52)
        self.input.setPlaceholderText('Insert link to video')
        self.input.returnPressed.connect(self.Info)
        self.input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {colors['fill']};
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;
                
                color: {colors['text']};
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
        icon.setPixmap(QPixmap(str(files['images']['png']['other']['link'])))
        icon.setScaledContents(True)

    def Text_Content(self, title: str):
        '''Блок названия контента'''
        # Иконка
        icon = QLabel(self.window)
        icon.setGeometry(21, 165, 44, 45)
        icon.setPixmap(QPixmap(str(files['images']['png']['other']['download'])))
        icon.setScaledContents(True)

        # Название
        text = QLabel(title, self.window)
        text.setGeometry(85, 165, 895, 20)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setStyleSheet(f'''
            QLabel {{
                color: {colors['text']};
                font-size: {font_big}px;
            }}
        ''')
        return text

    def Text_Status(self):
        '''Статус'''
        self.status = QLabel('Download status will be displayed here', self.window)
        self.status.setGeometry(85, 190, 895, 20)
        self.status.setStyleSheet(f'''
                QLabel {{
                    color: {colors['info']};
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

    def Block_Info(self, blocks: dict, number: str = '-') -> QLabel:
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
                font-size: {font_small}px;
            }}
        ''')
        return value

    def Button_Download_Video(self, button: dict):
        '''Кнопка скачивания видео'''
        self.button_download = QPushButton(button['title'], self.window)
        self.button_download.setGeometry(*button['geometry'])
        self.button_download.setToolTip(button['tooltip'])
        self.button_download.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_download.clicked.connect(self.Download_Video)
        self.button_download.setEnabled(False)
        self.button_download.setStyleSheet(f'''
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
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

    def Button_Stop(self, button: dict):
        '''Кнопка остановки скачивания видео'''
        self.button_stop = QPushButton(button['title'], self.window)
        self.button_stop.setGeometry(*button['geometry'])
        self.button_stop.setToolTip(button['tooltip'])
        self.button_stop.setIcon(QIcon(str(button['icon']).replace('\\', '/')))
        self.button_stop.setIconSize(QSize(30, 30))
        self.button_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_stop.clicked.connect(self.core.Stop_Download)
        self.button_stop.setStyleSheet(f'''
            QPushButton {{
                background-color: {colors['fill']};
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['text']};
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
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

    def Button_Settings(self, button: dict):
        '''Кнопка настроек'''
        self.button_settings = QPushButton(button['title'], self.window)
        self.button_settings.setGeometry(*button['geometry'])
        self.button_settings.setToolTip(button['tooltip'])
        self.button_settings.setIcon(QIcon(str(button['icon']).replace('\\', '/')))
        self.button_settings.setIconSize(QSize(30, 30))
        self.button_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_settings.clicked.connect(lambda: self.settings.Show())
        self.button_settings.setStyleSheet(f'''
            QPushButton {{
                background-color: {colors['fill']};
                border: 2px solid {colors['stroke']};
                border-radius: {border_radius_small}px;

                color: {colors['text']};
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
                font-size: {font_small}px;
                padding: 2px;
            }}
        ''')

    def Block_Preview(self):
        '''Блок превью'''
        # Основное окно
        preview = QPushButton(self.window)
        preview.setGeometry(20, 280, self.size_preview[0], self.size_preview[1])
        preview.setCursor(Qt.CursorShape.PointingHandCursor)
        preview.clicked.connect(self.Download_Preview)
        preview.setStyleSheet(f'''
            QPushButton {{
                background-color: #000000;
                border-radius: {border_radius_small}px;
            }}
        ''')

        # Ховер
        self.hover_icon = QLabel(preview)
        self.hover_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        dl_svg = QSvgRenderer(str(files['images']['svg']['buttons']['download_preview']))
        icon = QPixmap(
            icon_size, 
            icon_size
        )
        icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(icon)
        dl_svg.render(
            painter, 
            QRectF(0, 0, icon_size, icon_size))
        painter.end()
        self.hover_icon.setPixmap(icon)
        self.hover_icon.setGeometry(
            (self.size_preview[0] - icon_size) // 2,
            (self.size_preview[1] - icon_size) // 2,
            icon_size, icon_size
        )

        self.icon_effect = QGraphicsOpacityEffect(self.hover_icon)
        self.hover_icon.setGraphicsEffect(self.icon_effect)
        self.icon_effect.setOpacity(0)
        self.hover_overlay = QLabel(preview)
        self.hover_overlay.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.hover_overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # фигма Radial 
        self.hover_overlay.setStyleSheet(f'''
            QLabel {{
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                    stop:0 rgba(42, 41, 41, 0),
                    stop:1 #000000
                );
                border: none;
            }}
        ''')
        self.overlay_effect = QGraphicsOpacityEffect(self.hover_overlay)
        self.hover_overlay.setGraphicsEffect(self.overlay_effect)
        self.overlay_effect.setOpacity(0)


        def hover_state(shown):
            self.overlay_effect.setOpacity(shown)
            self.icon_effect.setOpacity(shown)
        slow = slow_graph()


        def hover(appear):
            self.appearing = appear
            self.anim.stop()
            self.anim.start()
        self.anim = QVariantAnimation(self.window)
        self.anim.setDuration(600)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.valueChanged.connect(
            lambda incel: hover_state(slow(float(incel))) if self.appearing else hover_state(1 - slow(float(incel)))
        )
        
        preview.enterEvent = lambda e: hover(True)
        preview.leaveEvent = lambda e: hover(False)

        # Размытие
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(10)
        self.blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.PerformanceHint)

        # Пустой фон
        self.blur = QLabel(preview)
        self.blur.setGeometry(0, 0, self.size_preview[0], self.size_preview[1])
        self.blur.setGraphicsEffect(self.blur_effect)
        self.blur.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
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
        self.image.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.image.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;
            }}
        ''')

        # Подгон размера
        scaled_pixmap = QPixmap(str(files['images']['png']['other']['preview'])).scaled(
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
        self.hover_overlay.raise_()
        self.hover_icon.raise_()

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
        self.title.setText(self.placeholder)

        self.button_download.setEnabled(False)

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

        def Thread():
            self.core.Prepare(self.input_url)
            self.core.title, self.core.video_link, self.core.site, self.core.id = self.core.Get_Video()

            self.core.Get_Preview()
            self.core.Get_Info()

        self.input_url = self.input.text()
        self.input.clear()

        thread = threading.Thread(target = Thread, daemon = True)
        thread.start()

    def Download_Preview(self):
        '''Скачивание превью'''
        thread = threading.Thread(target = self.core.Download_Preview, daemon = True)
        thread.start()

    def Download_Video(self):
        '''Скачивание видео'''
        thread = threading.Thread(target = self.core.Download_Video, daemon = True)
        thread.start()

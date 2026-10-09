# Deubaso Composifity
# Main

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import threading

# Локальные модули
from config import files, placeholder
from logger import Log
from presets import *
from settings import SETTINGS

log = Log()



class MAIN():
    '''Главное окно'''
    def __init__(self, core):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow()
        self.core = core
        self.settings = SETTINGS(self.window)

        # Отрисовка
        Window(self.window, f'{name} - Porn Parser', name)

        self.Block_Input()

        self.title = self.Text_Content(placeholder)
        self.status = self.Text_Status()

        self.Block_Progress_Bar()

        self.speed = self.Block_Info(Main_Layouts.Blocks()['speed'])
        self.max_speed = self.Block_Info(Main_Layouts.Blocks()['max_speed'])
        self.size = self.Block_Info(Main_Layouts.Blocks()['size'])
        self.quality = self.Block_Info(Main_Layouts.Blocks()['quality'])
        self.fps = self.Block_Info(Main_Layouts.Blocks()['fps'])
        self.duration = self.Block_Info(Main_Layouts.Blocks()['duration'])

        self.Button_Download_Video(Main_Layouts.Buttons()['download_video'])
        self.Button_Stop(Main_Layouts.Buttons()['stop'])
        self.Button_Settings(Main_Layouts.Buttons()['settings'])

        self.Block_Preview()

        self.window.show()

    def Block_Input(self):
        '''Блок строки ввода'''
        self.input = QLineEdit(self.window)
        self.input.setGeometry(margin, 95, length, size_big)
        self.input.setPlaceholderText('Insert link to video')
        self.input.returnPressed.connect(self.Search_Info)
        self.input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
                
                color: {colors['signal']['text']};
                font-size: {font_big}px;
                
                padding-left: 45px;
                padding-right: {border_radius_big}px;
            }}
            
            QLineEdit:hover {{
                background-color: {colors['tooltip']['fill']};
                border-color: {colors['tooltip']['stroke']};
            }}
        ''')

        icon = QLabel(self.input)
        icon.setGeometry(11, 11, size_icon.width(), size_icon.height())
        icon.setPixmap(QPixmap(str(files['images']['svg']['other']['link'])))
        icon.setScaledContents(True)

    def Text_Content(self, title: str):
        '''Блок названия контента'''
        # Иконка
        icon = QLabel(self.window)
        icon.setGeometry(21, 165, 44, 44)
        icon.setPixmap(QPixmap(str(files['images']['svg']['other']['download'])).scaled(
            44, 44,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

        # Название
        text = QLabel(title, self.window)
        text.setGeometry(85, 165, 895, 20)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setStyleSheet(f'''
            QLabel {{
                color: {colors['signal']['text']};
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
                    color: {colors['signal']['info']};
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
                color: {colors['signal'].get(type)};
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
        self.progress_bar.setGeometry(margin, 230, length, size_small)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(f'''
            QProgressBar {{
                background-color: {colors['other']['fill']};
                border-radius: {border_radius_big}px;
                
                color: {colors['signal']['text']};
                font-size: {font_big}px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['download']['start']}, 
                    stop:1 {colors['download']['end']}
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
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
            }}
            
            QFrame:hover {{
                background-color: {colors['tooltip']['fill']};
                border-color: {colors['tooltip']['stroke']};
            }}
        ''')

        # Название
        title = QLabel(blocks['title'], block)
        title.setGeometry(10, 10, 102, size_small)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;
            
                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
        ''')

        # Значение
        value = QLabel(number, block)
        value.setGeometry(10, 40, 102, size_small)
        value.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        setText = value.setText

        def Condition(text: str):
            '''Состояние'''
            color = colors['signal']['error'] if 'N/A' in text else colors['signal']['info']
            value.setStyleSheet(f'''
                QLabel {{
                    background: transparent;
                    border: none;
                
                    color: {color};
                    font-size: {font_small}px;
                }}
            ''')
            setText(text)

        value.setText = Condition
        Condition(number)
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
                    stop:0 {colors['download']['start']}, 
                    stop:1 {colors['download']['end']}
                );
                border: transparent;
                border-radius: {border_radius_small}px;
                
                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['download']['start_pressed']}, 
                    stop:1 {colors['download']['end_pressed']}
                );
                
                color: {colors['signal']['info']};
            }}
            
            QPushButton:disabled {{
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['download']['start_pressed']}, 
                    stop:1 {colors['download']['end_pressed']}
                );
                
                color: {colors['signal']['info']};
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

    def Button_Stop(self, button: dict):
        '''Кнопка остановки скачивания видео'''
        self.button_stop = QPushButton(self.window)
        self.button_stop.setGeometry(*button['geometry'])
        self.button_stop.setToolTip(button['tooltip'])
        self.button_stop.setIcon(QIcon(str(button['icon']).replace('\\', '/')))
        self.button_stop.setIconSize(size_icon)
        self.button_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_stop.clicked.connect(self.core.Stop_Download)
        self.button_stop.setEnabled(False)
        self.button_stop.setStyleSheet(f'''
            QPushButton {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
            }}
            
            QPushButton:hover {{
                background-color: {colors['tooltip']['fill']};
                border-color: {colors['tooltip']['stroke']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['other']['press']};
                border-color: {colors['other']['stroke']};
            }}
            
            QPushButton:disabled {{
                background-color: {colors['other']['press']};
                border-color: {colors['other']['stroke']};
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

    def Button_Settings(self, button: dict):
        '''Кнопка настроек'''
        self.button_settings = QPushButton(self.window)
        self.button_settings.setGeometry(*button['geometry'])
        self.button_settings.setToolTip(button['tooltip'])
        self.button_settings.setIcon(QIcon(str(button['icon']).replace('\\', '/')))
        self.button_settings.setIconSize(size_icon)
        self.button_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_settings.clicked.connect(lambda: self.settings.Show())
        self.button_settings.setStyleSheet(f'''
            QPushButton {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
            }}
            
            QPushButton:hover {{
                background-color: {colors['tooltip']['fill']};
                border-color: {colors['tooltip']['stroke']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['other']['press']};
                border-color: {colors['other']['stroke']};
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

    def Block_Preview(self):
        '''Блок превью'''
        preview = QPushButton(self.window)
        preview.setGeometry(margin, 280, size_preview[0], size_preview[1])
        preview.setCursor(Qt.CursorShape.PointingHandCursor)
        preview.clicked.connect(self.Download_Preview)
        preview.setStyleSheet(f'''
            QPushButton {{
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
        self.blur.setGeometry(0, 0, size_preview[0], size_preview[1])
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
        self.image.setGeometry(0, 0, size_preview[0], size_preview[1])
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
            QSize(size_preview[0], size_preview[1]),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled_pixmap)

        # Название сайта
        self.site_label = QLabel(preview)
        self.site_label.setGeometry(167, size_preview[1] - 42, 200, size_small)
        self.site_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.site_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.site_label.hide()
        self.site_label.setStyleSheet(f'''
            QLabel {{
                background-color: {colors['other']['fill']};
                border: none;
                border-radius: {border_radius_small}px;

                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
        ''')

        # Виньетка
        vignette = QLabel(preview)
        vignette.setGeometry(0, 0, size_preview[0], size_preview[1])
        vignette.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        vignette_pixmap = QPixmap(size_preview[0], size_preview[1])
        vignette_pixmap.fill(QColor(0, 0, 0, 150))
        vignette.setPixmap(vignette_pixmap)

        self.vignette_effect = QGraphicsOpacityEffect(vignette)
        self.vignette_effect.setOpacity(0.0)
        vignette.setGraphicsEffect(self.vignette_effect)

        # Иконка
        icon = QLabel(preview)
        icon.setGeometry(
            (size_preview[0] - size_big) // 2,
            (size_preview[1] - size_big) // 2,
            size_big,
            size_big
        )
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        icon.setPixmap(QPixmap(str(files['images']['svg']['other']['download'])).scaled(
            size_icon,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        icon.setStyleSheet(f'''
            QLabel {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
            }}
        ''')

        self.icon_effect = QGraphicsOpacityEffect(icon)
        self.icon_effect.setOpacity(0.0)
        icon.setGraphicsEffect(self.icon_effect)

        # Рамка
        border = QLabel(preview)
        border.setGeometry(1, 1, size_preview[0] - 2, size_preview[1] - 2)
        border.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        border.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: 2px solid {colors['tooltip']['stroke']};
                border-radius: {border_radius_small}px;
            }}
        ''')

        self.border_effect = QGraphicsOpacityEffect(border)
        self.border_effect.setOpacity(0.0)
        border.setGraphicsEffect(self.border_effect)

        # Анимации
        duration_in = 200
        duration_out = 100

        self.vignette_in = QPropertyAnimation(self.vignette_effect, b'opacity')
        self.vignette_in.setDuration(duration_in)
        self.vignette_in.setEndValue(1.0)
        self.vignette_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.icon_in = QPropertyAnimation(self.icon_effect, b'opacity')
        self.icon_in.setDuration(duration_in)
        self.icon_in.setEndValue(1.0)
        self.icon_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.border_in = QPropertyAnimation(self.border_effect, b'opacity')
        self.border_in.setDuration(duration_in)
        self.border_in.setEndValue(1.0)
        self.border_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.vignette_out = QPropertyAnimation(self.vignette_effect, b'opacity')
        self.vignette_out.setDuration(duration_out)
        self.vignette_out.setEndValue(0.0)
        self.vignette_out.setEasingCurve(QEasingCurve.Type.InCubic)

        self.icon_out = QPropertyAnimation(self.icon_effect, b'opacity')
        self.icon_out.setDuration(duration_out)
        self.icon_out.setEndValue(0.0)
        self.icon_out.setEasingCurve(QEasingCurve.Type.InCubic)

        self.border_out = QPropertyAnimation(self.border_effect, b'opacity')
        self.border_out.setDuration(duration_out)
        self.border_out.setEndValue(0.0)
        self.border_out.setEasingCurve(QEasingCurve.Type.InCubic)

        # Наведение
        preview.enterEvent = lambda event: self.Hover_Preview(True)
        preview.leaveEvent = lambda event: self.Hover_Preview(False)

        # Маска
        mask = QBitmap(QSize(size_preview[0], size_preview[1]))
        mask.fill(Qt.GlobalColor.color0)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.color1)
        painter.drawRoundedRect(0, 0, size_preview[0], size_preview[1], 10, 10)
        painter.end()

        preview.setMask(mask)

    def Hover_Preview(self, show: bool):
        '''Анимация при наведении на превью'''
        if show:
            self.vignette_in.start()
            self.icon_in.start()
            self.border_in.start()
        else:
            self.vignette_out.start()
            self.icon_out.start()
            self.border_out.start()

    def Update_Preview(self, preview_path: str = ''):
        '''Подгрузка нового превью'''
        load = QPixmap(preview_path)

        blur_pixmap = load.scaled(
            QSize(size_preview[0], size_preview[1]),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.blur.setPixmap(blur_pixmap)

        scaled_pixmap = load.scaled(
            QSize(size_preview[0], size_preview[1]),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled_pixmap)

    def Set_Site(self, site: str):
        '''Показ названия сайта'''
        self.site_label.setText(site)
        self.site_label.show()
        self.site_label.raise_()

    def Reset(self):
        '''Сброс метрик'''
        self.button_download.setEnabled(False)
        self.button_stop.setEnabled(False)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)

        self.site_label.hide()

        self.title.setText(placeholder)

        self.speed.setText('-')
        self.max_speed.setText('-')
        self.size.setText('-')
        self.quality.setText('-')
        self.fps.setText('-')
        self.duration.setText('-')

    def Search_Info(self):
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

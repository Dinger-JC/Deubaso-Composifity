# Deubaso Composifity: core
# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import math
import os
import re
import secrets
from datetime import timedelta, datetime
from fractions import Fraction
from pathlib import Path
from pprint import pprint
from urllib.parse import urlparse

# Сторонние библиотеки
import ffmpeg
import yt_dlp
from bs4 import BeautifulSoup
from curl_cffi import requests
from io import BytesIO
from mutagen.mp4 import MP4
from PIL import Image
from PySide6.QtCore import QObject, Signal
from yt_dlp.utils._utils import _UnsafeExtensionError

# Локальные модули
from config import *
from logger import Log, Timer

log = Log()



class SIGNALS(QObject):
    '''Сигналы'''
    signal_status = Signal(str, str)
    signal_title = Signal(str)
    signal_site = Signal(str)
    signal_preview = Signal(str)
    signal_speed = Signal(str)
    signal_max_speed = Signal(str)
    signal_size = Signal(str)
    signal_quality = Signal(str)
    signal_fps = Signal(str)
    signal_duration = Signal(str)
    signal_progress = Signal(int)
    signal_buttons = Signal(bool)



class CORE:
    '''Ядро'''
    def __init__(self):
        '''Инициализация'''
        self.signals = SIGNALS()
        self.Reset()

    def Convert_Bytes(self, value: int = 0, units: str = '') -> str:
        '''Конвертация байтов'''
        if value is None or value == 0:
            return 'N/A'
        if value < factor['KiB']:
            return f'{value} B' + units
        if value < factor['MiB']:
            num = value / factor['KiB']
            unit = 'KiB'
        elif value < factor['GiB']:
            num = value / factor['MiB']
            unit = 'MiB'
        else:
            num = value / factor['GiB']
            unit = 'GiB'

        if num < 10:
            precision = 3
        elif num < 100:
            precision = 2
        elif num < 1000:
            precision = 1
        else:
            precision = 0
        return f'{num:.{precision}f} {unit}' + units

    def Reset(self):
        '''Сброс метрик'''
        self.max_speed = 0
        self.cancel_download = False
        self.domain = None
        self.date = None
        self.id = None
        self.path = None
        self.cache_video_name = None
        self.cache_preview_name = None
        self.yt_dlp_options = None
        self.ffprobe_options = None
        self.response = None
        self.page = None
        self.config_site = None
        self.title = None
        self.video = None
        self.site = None
        self.preview = None
        self.tags = None

    def Stop_Download(self):
        '''Прерывание скачивания'''
        self.cancel_download = True

    def Aliases(self, url: str) -> str:
        '''Проверочные ссылки'''
        url_lower = url.lower()
        if url_lower in sites:
            url = sites[url_lower]['link']
        return url

    def Update_Config(self, url: str) -> bool:
        '''Обновление конфигурации для каждого видео'''
        self.signals.signal_status.emit('info', 'Checking...')
        log.info('Checking...')
        log.info(f'Link: {url}')

        # Проверка ссылки
        if not url.startswith(('http://', 'https://')):
            self.signals.signal_status.emit('error', 'Incorrect link')
            self.signals.signal_preview.emit(str(files['images']['png']['preview']))
            log.error('Incorrect link')
            return False

        self.Write_History(url)
        self.domain = urlparse(url).netloc
        self.site = next((name for name, info in sites.items() if self.Match_Domain(self.domain, info['domain'])), None)
        self.config_site = sites.get(self.site)
        self.date = datetime.now().strftime('%Y.%m.%d')
        self.id = secrets.token_hex(8)

        # Директория
        self.path = Path(settings['path'])
        self.path.mkdir(parents = True, exist_ok = True)
        self.cache_video_name = f'{self.path / secrets.token_urlsafe(24)}.mp4'
        self.cache_preview_name = f'{self.path / secrets.token_urlsafe(24)}.png'

        # Заголовки HTTP-запросов
        headers = {
            'sec-ch-ua': f'"Not_A Brand";v="8", "Chromium";v="{chrome}", "Google Chrome";v="{chrome}"', # Движок
            'sec-ch-ua-mobile': '?0', # Платформа
            'sec-ch-ua-platform': '"Windows"', # ОС
            'upgrade-insecure-requests': '1', # Просьба о защите
            'user-agent': self.Generate_User_Agent(), # Имитация браузера Chrome (TLS/HTTP2)
            'accept': '*/*', # Фильтр формата данных
            'sec-fetch-site': 'cross-site', # Запрос идет на другой домен
            'sec-fetch-mode': 'cors', # Режим запроса без CORS
            'sec-fetch-user': '?1', # Имитация активного действия
            'sec-fetch-dest': 'video', # Цель запроса видео
            'referer': f'https://{self.domain}/', # C какой страницы пришел запрос
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8', # Языки
            'range': 'bytes=0-' # Запрос на подгрузку потока
        }

        # Настройки yt_dlp
        self.yt_dlp_options = {
            'http_headers': headers, # Заголовки HTTP-запросов
            'progress_hooks': [self.Progress_Hook], # Отслеживание прогресса загрузки
            'ffmpeg_location': str(files['bin']['ffmpeg']), # Путь к ffmpeg
            'outtmpl': self.cache_video_name, # Путь сохраняемого файла
            'format': 'bestvideo+bestaudio/best', # Качество видео
            'merge_output_format': 'mp4', # Формат после загрузки
            'socket_timeout': timeout, # Время ожидания ответа от сервера (в секундах)
            'sleep_interval': 0, # Минимальная случайная пауза между загрузками (в секундах)
            'max_sleep_interval': 2, # Максимальная случайная пауза между запросами (в секундах)
            'retries': retries, # Количество попыток переподключения при ошибке загрузки файла
            'fragment_retries': 5, # Количество попыток загрузки каждого отдельного фрагмента видео
            'rm_cached_metadata': True, # Очистка метаданных из кэша перед началом загрузки
            'nocheckcertificate': False, # Проверка SSL-сертификатов
            'quiet': True, # Лог
            'verbose': False # Подробный лог
        }

        # Настройки ffprobe
        self.ffprobe_options = {
            'headers': ''.join([f'{k}: {v}\r\n' for k, v in headers.items()]), # Заголовки HTTP-запросов
            'analyzeduration': '10000000', # Время на чтение данных (в микросекундах)
            'probesize': '10000000', # Максимальный объем данных для анализа (в байтах)
            'rw_timeout': '15000000', # Общее время на операцию (в микросекундах)
            'reconnect_delay_max': '5', # Максимальное время ожидания (в секундах)
            'tls_verify': '1', # Проверка SSL-сертификатов
            'reconnect': '1', # Автоматическое переподключение
            'seekable': '0', # Чтение потока
            'reconnect_streamed': '1' # Автоматическое переподключение для стримов
        }
        return True

    def Match_Domain(self, domain: str, target: str) -> bool:
        '''Совпадение поддоменов'''
        return domain == target or domain.endswith(f'.{target}')

    def Generate_User_Agent(self) -> str:
        '''Генерация случайного браузера'''
        patch_version = secrets.choice([33, 69, 70, 71, 85, 86, 87, 108, 109, 110, 139, 140, 141, 204, 205, 206, 264, 265, 266, 267])
        chrome_version = f'{chrome}.0.6778.{patch_version}'
        user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
        return user_agent

    def Write_History(self, url: str):
        '''Запись в историю'''
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%B')
        date = now.strftime('%Y.%m.%d')
        time = now.strftime('%H:%M:%S')

        if settings['history'] == 1:
            if files['data']['history'].is_file():
                with open(files['data']['history'], 'r', encoding = 'utf-8') as file:
                    data = json.load(file)
            else:
                data = {}

            year_dict = data.setdefault(year, {})
            month_dict = year_dict.setdefault(month, {})
            day_dict = month_dict.setdefault(date, {})
            day_dict[time] = url

            with open(files['data']['history'], 'w', encoding = 'utf-8') as file:
                json.dump(data, file, indent = 4, ensure_ascii = False)

    def Progress_Hook(self, data):
        '''Загрузка'''
        if self.cancel_download:
            self.signals.signal_speed.emit('-')
            raise Exception('Download aborted')

        if data['status'] == 'downloading':
            speed = data.get('speed') or 0
            volume = data.get('total_bytes') or data.get('total_bytes_estimate')
            downloaded = data.get('downloaded_bytes', 0)
            percent = float(round(downloaded / volume * 100, 2))

            if speed > self.max_speed:
                self.max_speed = speed

            try:
                current_percent = int(percent)
            except Exception:
                current_percent = 0
            visual_value = max(4, current_percent) if current_percent > 0 else 0

            self.signals.signal_progress.emit(visual_value)
            self.signals.signal_speed.emit(f'{self.Convert_Bytes(speed, '/s')}')
            self.signals.signal_max_speed.emit(f'{self.Convert_Bytes(self.max_speed, '/s')}')
            self.signals.signal_size.emit(f'{self.Convert_Bytes(volume)}')

        elif data['status'] == 'finished':
            self.signals.signal_progress.emit(100)
            self.signals.signal_status.emit('info', 'File is being compiled...')
            log.info('File is being compiled...')

    def Check_Link(self) -> bool:
        '''Проверка ответа страницы'''
        code = self.response.status_code
        errors = {
            400: 'Incorrect request: check validity of entered data',
            401: 'Authorization is required: log in to your account to gain access',
            403: 'Access denied: server rejected your request',
            404: 'Page not found: check address or it has been deleted',
            408: 'Timeout period has expired: server has been waiting for too long',
            410: 'Resource is gone: requested object has been permanently removed from server',
            429: 'Too many requests: you have exceeded limit, please wait',
            500: 'Internal server error: something went wrong on server side',
            502: 'Connection error: server received an incorrect response from upstream node',
            503: 'Server is temporarily unavailable due to technical work or high load'
        }

        if code in [200, 206]:
            return True

        self.Reset()

        full_message = f'Error {code}. {errors.get(code, '?')}'
        self.signals.signal_status.emit('error', full_message)
        self.signals.signal_preview.emit(str(files['images']['png']['preview']))
        log.error(full_message)
        return False

    def Connection(self, url: str) -> bool:
        '''Соединение'''
        try:
            url = self.Aliases(url)

            if not self.Update_Config(url):
                return False

            self.response = requests.get(url, impersonate = f'chrome{chrome}', timeout = timeout)
            self.page = BeautifulSoup(self.response.text, 'html.parser')

            if not self.Check_Link():
                return False

            self.signals.signal_status.emit('info', 'Connection...')
            log.info('Connection...')
            return True

        except requests.exceptions.ConnectionError:
            self.signals.signal_status.emit('error', f'Connection error to "{self.domain}": resource may be blocked and may require VPN or proxy')
            self.signals.signal_preview.emit(str(files['images']['png']['preview']))
            log.error(f'Connection error to "{self.domain}": resource may be blocked and may require VPN or proxy')
            return False

        except requests.exceptions.Timeout:
            self.signals.signal_status.emit('error', f'Exceeded waiting time for a response from "{self.domain}"')
            self.signals.signal_preview.emit(str(files['images']['png']['preview']))
            log.error(f'Exceeded waiting time for a response from "{self.domain}"')
            return False

    def Get_Title(self):
        '''Получение названия'''
        try:
            self.title = self.page.find('title').text
            if 'title' in self.config_site:
                self.title = re.sub(self.config_site['title'], '', self.title, flags = re.IGNORECASE).strip()

            self.signals.signal_title.emit(self.title)
            log.info(f'Name: {self.title}')

        except Exception as e:
            self.signals.signal_status.emit('warning', f'Error get title: {e}')
            log.warning(f'Error get title: {e}')

    def Get_Video(self) -> bool:
        '''Получение видео'''
        domain = self.config_site['domain']

        if domain == sites['strip2']['domain']:
            source = [node.get('href') for node in self.page.select('a[href*="vps402.strip2.co.mp4"]') if node.get('href')]
            self.video = next((i for i in source if f'/x{len(source) - 1}/' in str(i)), source[-1])

        elif domain == sites['analmedia']['domain']:
            source = self.page.select_one('video source')
            self.video = source.get('src', '') if source else ''

        elif domain == sites['rule34video']['domain']:
            source = self.page.select('a.tag_item')
            self.video = next((node.get('href') for tag in tags for node in source if tag in node.text.lower()), '')

        elif domain == sites['xgroovy']['domain']:
            source = self.page.select('source')
            self.video = next((node.get('src') for tag in tags for node in source if node.get('title') == tag), '')

        elif domain == sites['pornobomba']['domain']:
            source = re.findall(r'https?://[^\s"\'<>]+?/get_file/\d+/[0-9a-f]+/\d+/\d+/\d+\.mp4/?', str(self.page))
            self.video = source[0] if source else ''

        if self.video == '' or self.video == None:
            self.signals.signal_status.emit('error', 'Video extraction error')
            self.signals.signal_preview.emit(str(files['images']['png']['preview']))
            log.error('Video extraction error')
            return False

        log.info(f'Video: {self.video}')

    def Get_Tags(self):
        '''Получение тегов'''
        links = self.page.select(self.config_site['tags_pattern'])
        self.tags = ', '.join([link.text.strip() for link in links])
        log.info(f'Tags: {self.tags}')

    def Get_Preview(self):
        '''Получение превью'''
        try:
            image = None
            pattern = sites[self.site]['preview_pattern']

            if '{tag}' in pattern:
                for tag in tags:
                    match = re.search(pattern.replace('{tag}', re.escape(tag)), str(self.page))
                    if match:
                        image = match.group(0)
                        break

            else:
                match = re.search(pattern, str(self.page))
                image = match.group(0) if match else None
                if image:
                    best = re.sub(r'_m(\.mp4\.jpg)$', r'\1', image)
                    image = best

            self.preview = requests.get(image, impersonate = f'chrome{chrome}', timeout = timeout).content
            with Image.open(BytesIO(self.preview)) as preview:
                preview.save(self.cache_preview_name)

            self.signals.signal_site.emit(self.site)
            self.signals.signal_preview.emit(self.cache_preview_name)
            log.info(f'Preview: {image}')

        except Exception as e:
            self.signals.signal_status.emit('warning', f'Error get preview: {e}')
            log.warning(f'Error get preview: {e}')

    def Get_Info(self):
        '''Получение дополнительной информации'''
        self.signals.signal_status.emit('info', 'Getting info...')
        log.info('Getting info...')

        try:
            ffprobe_video_info = ffmpeg.probe(self.video, cmd = files['bin']['ffprobe'],  **self.ffprobe_options)
            video_stream = next((stream for stream in ffprobe_video_info['streams'] if stream['codec_type'] == 'video'), None)

            try:
                width = video_stream['width']
                height = video_stream['height']
                quality = f'{int(width)}x{int(height)}'
                log.info(f'Quality: {quality}')
            except (KeyError, TypeError, ValueError):
                quality = 'N/A'
                log.warning(f'Quality: {quality}')

            try:
                fps = str(math.ceil(float(Fraction(video_stream['avg_frame_rate']))))
                log.info(f'FPS: {fps}')
            except (KeyError, TypeError, ValueError, ZeroDivisionError):
                fps = 'N/A'
                log.warning(f'FPS: {fps}')

            try:
                duration = str(timedelta(seconds = float(video_stream['duration']))).split('.')[0]
                log.info(f'Duration: {duration}')
            except (KeyError, TypeError, ValueError):
                duration = 'N/A'
                log.warning(f'Duration: {duration}')

            self.signals.signal_quality.emit(quality)
            self.signals.signal_fps.emit(fps)
            self.signals.signal_duration.emit(duration)
            self.signals.signal_status.emit('good', 'Video is ready!')
            log.info('Video is ready!')

        except Exception as e:
            self.signals.signal_status.emit('warning', f'Error get info: {e}')
            log.warning(f'Error get info: {e}')

        finally:
            self.signals.signal_buttons.emit(True)

    def Get_All_Data(self, url: str):
        '''Получение всех данных'''
        if not self.Connection(url):
            return

        if self.site is None:
            self.signals.signal_status.emit('warning', f'Downloads are only available from {placeholder}')
            self.signals.signal_preview.emit(str(files['images']['png']['preview']))
            log.warning(f'Downloads are only available from {placeholder}')
            return

        self.Get_Title()

        validate = self.Get_Video()
        if validate is False:
            return

        self.Get_Tags()
        self.Get_Preview()
        self.Get_Info()

    def Edit_Video(self, name: str, title: str):
        '''Редактирование видео'''
        try:
            video = MP4(name)
            video.delete()
            video['\xa9nam'] = title
            video['\xa9cmt'] = self.tags
            video.save()

        except Exception as e:
            self.signals.signal_status.emit('error', f'Error edit video: {e}')
            log.error(f'Error edit video: {e}')

    @Timer
    def Download_Video(self):
        '''Скачивание видео'''
        if self.video == None:
            return

        _UnsafeExtensionError._enabled = False
        aborted = False
        self.cancel_download = False
        self.signals.signal_status.emit('info', 'Downloading videos...')
        log.info('Downloading videos...')

        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
                video.download([self.video])

            final_video_name = self.path / f'{self.date} {self.site} [VIDEO_{self.id}].mp4'
            os.rename(self.cache_video_name, final_video_name)
            self.Edit_Video(final_video_name, self.title)

            self.signals.signal_speed.emit('-')
            self.signals.signal_buttons.emit(False)
            self.signals.signal_status.emit('good', f'Video downloaded: {str(final_video_name).replace('\\', '/')}')
            log.info(f'Video downloaded: {str(final_video_name).replace('\\', '/')}')

        except Exception as e:
            if 'Download aborted' in str(e):
                aborted = True
                self.signals.signal_status.emit('warning', 'Download aborted')
                log.warning('Download aborted')
            else:
                self.signals.signal_status.emit('error', f'Error download video: {e}')
                log.error(f'Error download video: {e}')

        finally:
            try:
                os.remove(self.cache_preview_name)
            except Exception:
                pass

            _UnsafeExtensionError._enabled = True
            if not aborted:
                self.Reset()

    def Download_Preview(self):
        '''Скачивание превью'''
        if self.preview == None:
            return

        try:
            final_preview_name = self.path / f'{self.site} - {self.date} [PREVIEW_{self.id}].png'
            image = Image.open(BytesIO(self.preview))
            image.save(final_preview_name, format = 'PNG')
            self.signals.signal_status.emit('good', f'Preview downloaded: {str(final_preview_name).replace('\\', '/')}')
            log.info(f'Preview downloaded: {final_preview_name}')

        except Exception as e:
            self.signals.signal_status.emit('warning', f'Error download preview: {e}')
            log.warning(f'Error download preview: {e}')

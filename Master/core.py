# Parser Deubaso Composifity
# Copyright (c) 2026 Dinger_JC
# Master functionality



# Стандартные библиотеки
import json
import math
import os
import random
import re
import string
import subprocess
import sys
import threading
from datetime import timedelta, datetime
from fractions import Fraction
from pathlib import Path
from pprint import pp
from urllib.parse import urlparse

# Сторонние библиотеки
packages = [
    'python-ffmpeg',
    'yt-dlp',
    'beautifulsoup4',
    'curl-cffi',
    'PySide6',
    'mutagen'
]

try:
    import ffmpeg
    import yt_dlp
    from bs4 import BeautifulSoup
    from curl_cffi import requests
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from mutagen.mp4 import MP4, MP4FreeForm
except ImportError:
    print('The required modules are missing. Module installation begins...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages])
    import ffmpeg
    import yt_dlp
    from bs4 import BeautifulSoup
    from curl_cffi import requests
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from mutagen.mp4 import MP4, MP4FreeForm

# Локальные модули
try:
    from logger import Log
    log = Log(__name__)
except ImportError:
    print('Failed to import the logger. It may be missing.')
    sys.exit(0)



class Core:
    '''Ядро парсера'''
    def __init__(self):
        '''Инициализация'''
        log.info('Start')

        # Проверка файлов
        self.absolute_path = os.path.dirname(os.path.abspath(__file__))
        self.files: dict = {
            'data': os.path.join(self.absolute_path, 'data.json'),
            'sites': os.path.join(self.absolute_path, 'sites.json'),
            'ffmpeg': os.path.join(self.absolute_path, 'ffmpeg.exe'),
            'ffprobe': os.path.join(self.absolute_path, 'ffprobe.exe'),
            'icon': os.path.join(self.absolute_path, 'icons', 'icon.png'),
            'link': os.path.join(self.absolute_path, 'icons', 'link.png'),
            'download': os.path.join(self.absolute_path, 'icons', 'download.png'),
            'settings': os.path.join(self.absolute_path, 'icons', 'settings.png'),
            'preview': os.path.join(self.absolute_path, 'icons', 'preview.png')
        }
        self.RequiredFiles()

        # Поддерживаемые сайты
        with open(self.files['sites'], encoding = 'utf-8') as file:
            self.sites: dict = json.load(file)

        # Директория
        self.path: Path = Path(r'D:\Saved Videos')
        self.path.mkdir(parents = True, exist_ok = True)
        self.temp_preview: str = f'{self.path / 'preview_temp'}.jpg'

        # Основное
        self.chrome: str = '131'
        self.max_speed: float = 0
        self.yt_dlp_options: dict = None

    def RequiredFiles(self):
        '''Проверка наличия необходимых файлов'''
        link: str = 'https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45'
        error = False

        for name, path in self.files.items():
            if not os.path.exists(path):
                log.critical(f'The "{path}" file was not found.')
                if name == 'ffmpeg' or name == 'ffprobe':
                    log.critical(f'You can download it here: {link}')
                error = True

        if error:
            log.critical('The program cannot be run due to missing files.')
            os._exit(0)

    def Link(self, url: str) -> str:
        '''Извлечение ссылки'''
        with open(self.files['data'], encoding = 'utf-8') as file:
            links: dict = json.load(file)
        presets: dict = links['videos']

        if url in links.get('videos'):
            url: str = presets[url]

        return url

    def UpdateConfig(self, url: str):
        '''Обновление конфигурации для каждого видео'''
        # Проверка ссылки
        self.gui.Status('status', 'Checking...')
        log.info('[CHECKING]')
        log.info(f'| Link: {url}')
        if not re.search(r'^https?://[\w\.-]+\/.*(video|watch).*', url):
            self.yt_dlp_options: dict = None
            self.gui.UpdatePreview(self.files['preview'])
            self.gui.Status('warning', 'Incorrect link. This link could not be found.')
            log.error('Incorrect link. This link could not be found.')
            sys.exit(0)

        # Название сайта
        self.domain: str = urlparse(url).netloc
        self.gui.Site(f'{self.domain}')
        log.info(f'| Site: {self.domain}')

        # Название кэша
        self.symbols: str = string.ascii_letters + string.digits + '_' * 5 + '-' * 5
        self.random_name: str = ''.join(random.choice(self.symbols) for _ in range(32))
        self.cache_name: str = f'{self.path / self.random_name}.mp4'

        # Заголовки HTTP-запросов
        self.headers: dict = {
            # Движок
            'sec-ch-ua': '"Not_A Brand";v="8", '
                f'"Chromium";v="{self.chrome}", '
                f'"Google Chrome";v="{self.chrome}"',
            'sec-ch-ua-mobile': '?0', # Платформа
            'sec-ch-ua-platform': '"Windows"', # ОС
            'upgrade-insecure-requests': '1', # Просьба о защите
            # Имитация браузера Chrome (TLS/HTTP2)
            'user-agent': 'Mozilla/5.0'
                '(Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                f'Chrome/{self.chrome}.0.0.0 '
                'Safari/537.36',
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
        self.yt_dlp_options: dict = {
            'http_headers': self.headers, # Заголовки HTTP-запросов
            'progress_hooks': [self.ProgressBar], # Отслеживание прогресса загрузки
            'ffmpeg_location': self.files['ffmpeg'], # Путь ffmpeg
            'outtmpl': self.cache_name, # Путь сохраняемого файла
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Качество видео
            'merge_output_format': 'mp4', # Формат после загрузки
            'socket_timeout': 30, # Время ожидания ответа от сервера (в секундах)
            'sleep_interval': 0, # Минимальная случайная пауза между загрузками (в секундах)
            'max_sleep_interval': 2, # Максимальная случайная пауза между запросами (в секундах)
            'retries': 5, # Количество попыток переподключения при ошибке загрузки файла
            'fragment_retries': 5, # Количество попыток загрузки каждого отдельного фрагмента видео
            'rm_cached_metadata': True, # Очистка метаданных из кэша перед началом загрузки
            'nocheckcertificate': True, # Игнорировать ошибки проверки SSL-сертификатов
            'quiet': True, # Лог
            'verbose': False # Подробный лог
        }

        # Настройки ffprobe
        self.ffprobe_options: dict = {
            'headers': ''.join([f'{k}: {v}\r\n' for k, v in self.headers.items()]), # Заголовки HTTP-запросов
            'analyzeduration': '10000000', # Время на чтение данных (в микросекундах)
            'probesize': '10000000', # Максимальный объем данных для анализа (в байтах)
            'rw_timeout': '15000000', # Общее время на операцию (в микросекундах)
            'reconnect_delay_max': '5', # Максимальное время ожидания (в секундах)
            'tls_verify': '0', # Отключает проверку SSL-сертификатов
            'reconnect': '1', # Автоматическое переподключение
            'seekable': '0', # Чтение потока последовательно
            'reconnect_streamed': '1' # Автоматическое переподключение для стримов
        }

    def FormatUnits(self, value: int = 0, format: str = '') -> str:
        '''Конвертация байтов'''
        factor: dict = {'KiB': 1024, 'MiB': 1024 ** 2, 'GiB': 1024 ** 3}

        if value is None or value == 0:
            return 'N/A'
        if value < factor['KiB']:
            return f'{value} B' + format
        if value < factor['MiB']:
            return f'{value / factor['KiB']:.2f} KiB' + format
        if value < factor['GiB']:
            return f'{value / factor['MiB']:.2f} MiB' + format
        return f'{value / factor['GiB']:.2f} GiB' + format

    def File(self):
        '''Создание уникального имени файла'''
        counter = 1
        while True:
            self.final_name: str = Path(self.path) / f'Video-{counter} ({self.site}).mp4'
            if not self.final_name.exists():
                os.rename(self.cache_name, self.final_name)
                break
            counter += 1

    def ProgressBar(self, data):
        '''Индикатор загрузки'''
        if data['status'] == 'downloading':
            speed: int = data.get('speed') or 0
            volume: int = data.get('total_bytes') or data.get('total_bytes_estimate')
            downloaded: int = data.get('downloaded_bytes', 0)
            percent: float = float(round(downloaded / volume * 100, 2))

            if speed > self.max_speed:
                self.max_speed = speed

            try:
                current_percent = int(percent)
            except (ValueError, TypeError):
                current_percent = 0
            visual_value = max(4, current_percent) if current_percent > 0 else 0

            self.gui.progress_bar.setTextVisible(True)
            self.gui.progress_bar.setValue(visual_value)

            self.gui.speed.setText(f'{self.FormatUnits(speed, '/s')}')
            self.gui.max_speed.setText(f'{self.FormatUnits(self.max_speed, '/s')}')
            self.gui.size.setText(f'{self.FormatUnits(volume)}')

        elif data['status'] == 'finished':
            self.File()

    def CheckLink(self):
        '''Проверка ответа страницы'''
        code: int = self.response.status_code
        errors: dict = {
            400: 'Incorrect request. Check the validity of the entered data.',
            401: 'Authorization is required. Log in to your account to gain access.',
            403: 'Access denied. The server rejected the request.',
            404: 'The page could not be found. Check the address or it has been deleted.',
            408: 'The waiting time has expired. The server has been waiting for too long.',
            429: 'Too many requests. You have exceeded the limit, please wait a moment.',
            500: 'Internal server error. Something went wrong on the server.',
            502: 'Connection error. The server received an incorrect response from the upstream node.',
            503: 'The server is temporarily overloaded. Technical work or high load.'
        }

        if code in [200, 206]:
            return

        if code in errors:
            self.gui.Status('warning', f'Error [{code}]: {errors[code]}')
            log.error(f'Error [{code}]: {errors[code]}')
        else:
            self.gui.Status('warning', f'Error {code}')
            log.error(f'Error {code}')

        sys.exit(0)

    def Data(self, url: str):
        '''Получение данных с сайта'''
        # Проверка сайта
        try:
            self.UpdateConfig(url)
            self.response = requests.get(url, timeout = 30, impersonate = f'chrome{self.chrome}')
            self.CheckLink()
            self.gui.Status('status', 'Getting basic information...')
            log.info('[GETTING BASIC INFORMATION]')
        except requests.exceptions.ConnectionError:
            self.yt_dlp_options: dict = None
            self.gui.Site('')
            self.gui.UpdatePreview(self.files['preview'])
            self.gui.Status('warning', f'Connection error to "{self.domain}". The resource may be blocked and may require a VPN or Proxy.')
            log.error(f'Connection error to "{self.domain}". The resource may be blocked and may require a VPN or Proxy.')
            sys.exit(0)
        except requests.exceptions.Timeout:
            self.yt_dlp_options: dict = None
            self.gui.Site('')
            self.gui.UpdatePreview(self.files['preview'])
            self.gui.Status('warning', f'Exceeded the waiting time for a response from "{self.domain}".')
            log.error(f'Exceeded the waiting time for a response from "{self.domain}".')
            sys.exit(0)

        self.page = BeautifulSoup(self.response.text, 'html.parser')
        self.video_url: str = None

        if self.domain == self.sites['Strip2']['domain']:
            raw_title: str = self.page.find('title').text
            self.title: str = re.sub(r'\s*[-–—]\s*Strip2.co\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site: str = 'Strip2'

            links = []
            self.video_url = self.page.find_all('a', href = True)
            for link in self.video_url:
                if 'vps402.strip2.co.mp4' in link['href']:
                    links.append(link['href'])

            for i, href in enumerate(links):
                find_link: str = str(href)
                if find_link and f'/x{len(links) - 1}/' in find_link:
                    self.video_url: str = find_link

        elif self.domain == self.sites['XGroovy']['domain']:
            raw_title: str = self.page.find('title').text
            self.title: str = raw_title

            tags = ['4k', '1080p', '720p', '480p', '240p']
            for tag in tags:
                video = self.page.find('source', title = tag)
                if video:
                    self.video_url = video.get('src')
                    break

        elif self.domain == self.sites['AnalMedia']['domain']:
            raw_title: str = self.page.find('title').text
            self.title: str = re.sub(r'\s*[-–—]\s*AnalMedia\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site: str = 'AnalMedia'

            video: str = self.page.find('video')
            self.video_url: str = video.find('source')['src']

        else:
            self.gui.Site('')
            self.gui.Status('warning', 'Downloads are only available from Strip2, XGroovy, and AnalMedia.')
            log.error('Downloads are only available from Strip2, XGroovy, and AnalMedia.')
            sys.exit(0)

        self.gui.title.setText(self.title)

        log.info(f'| Name: {self.title}')
        log.info(f'| Direct link: {self.video_url}')

        # Обновление
        self.gui.speed.setText('-')
        self.gui.max_speed.setText('-')
        self.gui.size.setText('-')

    def Preview(self):
        '''Получение превью'''
        if self.domain == self.sites['Strip2']['domain']:
            self.image: str = re.search(self.sites['Strip2']['pattern'], str(self.page)).group(0)
            with open(self.temp_preview, 'wb') as preview:
                preview.write(requests.get(self.image).content)
            self.gui.UpdatePreview(self.temp_preview)

        elif self.domain == self.sites['XGroovy']['domain']:
            self.image: str = re.search(self.sites['XGroovy']['pattern'], str(self.page)).group(0)
            with open(self.temp_preview, 'wb') as preview:
                preview.write(requests.get(self.image).content)
            self.gui.UpdatePreview(self.temp_preview)

        elif self.domain == self.sites['AnalMedia']['domain']:
            self.image: str = re.search(self.sites['AnalMedia']['pattern'], str(self.page)).group(0)
            with open(self.temp_preview, 'wb') as preview:
                preview.write(requests.get(self.image).content)
            self.gui.UpdatePreview(self.temp_preview)

        log.info(f'| Preview: {self.image}')

    def MoreInfo(self):
        '''Получение дополнительной информации'''
        self.gui.Status('status', 'Getting additional information...')
        log.info('[GETTING ADDITIONAL INFORMATION]')

        video_info: dict = ffmpeg.probe(self.video_url, **self.ffprobe_options)
        video_stream: dict = next((stream for stream in video_info['streams'] if stream['codec_type'] == 'video'), None)

        width: int = video_stream.get('width', 0)
        height: int = video_stream.get('height', 0)
        fps: str = f'{math.ceil(float(Fraction(video_stream.get('avg_frame_rate', 'N/A'))))}'
        raw_duration: float = video_stream.get('duration')
        duration: str = str(timedelta(seconds = float(raw_duration))).split('.')[0] if raw_duration else 'N/A'

        self.gui.quality.setText(f'{width}x{height}')
        self.gui.fps.setText(fps)
        self.gui.duration.setText(duration)

        log.info(f'| Quality: {width}x{height}')
        log.info(f'| FPS: {fps}')
        log.info(f'| Duration: {duration}')

        self.gui.Status('status', 'Video is ready to download!')

    def EditTags(self):
        '''Редактирование тегов'''
        tags = MP4(self.final_name)
        tags.delete()
        tags['\xa9too'] = 'Parser Deubaso Composifity' # Кодировщик
        tags['\xa9nam'] = self.title # Название
        tags['\xa9cmt'] = 'Developer - https://github.com/Dinger-JC/Deubaso-Composifity' # Комментарий
        tags['\xa9ART'] = 'Parser Deubaso Composifity' # Исполнитель
        tags['\xa9wrt'] = f'Site - {self.domain}' # Композитор
        tags['\xa9gen'] = 'Porn' # Жанр
        tags.save()

    def DownloadVideo(self):
        '''Скачивание видео'''
        if not self.yt_dlp_options or not self.video_url:
            self.gui.Status('warning', 'The link to the video is missing.')
            log.error('The link to the video is missing.')
            sys.exit(0)

        self.gui.Status('status', 'Downloading videos...')
        log.info('[DOWNLOADING VIDEOS]')

        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
                video.download([self.video_url])
            self.EditTags()
            self.gui.speed.setText('-')
            self.gui.Status('status', f'Downloaded in {str(self.final_name).replace('\\', '/')}')
            log.info(f'| Downloaded in {self.final_name}')
        except yt_dlp.utils.DownloadError as e:
            self.gui.Status('warning', f'Video download error: {e}')
            log.error(f'Video download error: {e}')
            sys.exit(0)
        except OSError as e:
            self.gui.Status('warning', f'System error: {e}')
            log.error(f'System error: {e}')
            sys.exit(0)
        finally:
            os.remove(self.temp_preview)

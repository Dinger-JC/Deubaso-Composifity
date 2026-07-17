# Parser Deubaso Composifity
# Master functionality

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import math
import os
import re
import secrets
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
    'ffmpeg-python',
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
    from mutagen.mp4 import MP4

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
    from mutagen.mp4 import MP4

# Локальные модули
try:
    from logger import Log
    log = Log(__name__)

except ImportError:
    print('Failed to import the logger. It may be missing.')
    sys.exit(1)



class CORE:
    '''Ядро'''
    def __init__(self):
        '''Инициализация'''
        # Необходимые файлы
        self.file_path = Path(__file__).resolve().parent.parent
        self.files = {
            'settings': str(self.file_path / 'config' / 'settings.json'),
            'sites': str(self.file_path / 'config' / 'sites.json'),
            'ffmpeg': str(self.file_path / 'bin' / 'ffmpeg.exe'),
            'ffprobe': str(self.file_path / 'bin' / 'ffprobe.exe'),
            'icon_icon': str(self.file_path / 'assets' / 'icon.png'),
            'link_icon': str(self.file_path / 'assets' / 'link.png'),
            'download_icon': str(self.file_path / 'assets' / 'download.png'),
            'stop_icon': str(self.file_path / 'assets' / 'stop.png'),
            'settings_icon': str(self.file_path / 'assets' / 'settings.png'),
            'preview_icon': str(self.file_path / 'assets' / 'preview.png')
        }
        self.Required_Files()

        # Второстепенные файлы
        self.file_history = '../data/history.json'
        self.file_videos = '../data/videos.json'

        # Настройки
        with open(self.files['settings'], encoding = 'utf-8') as file:
            self.settings = json.load(file)

        # Поддерживаемые сайты
        with open(self.files['sites'], encoding = 'utf-8') as file:
            self.sites = json.load(file)

        # Директория
        self.path: Path = Path(self.settings['path'])
        self.path.mkdir(parents = True, exist_ok = True)
        self.temp_preview = f'{self.path / 'preview_temp'}.jpg'

        # Основное
        self.chrome = '131'
        self.timeout = 30
        self.max_speed = 0
        self.yt_dlp_options = None
        self.video_url = None
        self.cancel_download = False
        self.factor = {'KiB': 1024, 'MiB': 1024 ** 2, 'GiB': 1024 ** 3}

    def Required_Files(self):
        '''Проверка наличия необходимых файлов'''
        link = 'https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45'
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
        with open(self.file_videos, encoding = 'utf-8') as file:
            videos = json.load(file)
        presets = videos

        if url in videos:
            url = presets[url]
        return url

    def Update_Config(self, url: str):
        '''Обновление конфигурации для каждого видео'''
        self.gui.Status('status', 'Checking...')
        log.info('[CHECKING]')
        log.info(f'| Link: {url}')

        # Проверка ссылки
        if not re.search(r'^https?://[\w\.-]+\/.*(video|watch).*', url):
            self.yt_dlp_options = None
            self.gui.Update_Preview(self.files['preview_icon'])
            self.gui.Status('warning', 'Incorrect link. This link could not be found.')
            log.error('Incorrect link. This link could not be found.')
            sys.exit(1)

        self.History(url) # Запись в историю
        self.domain = urlparse(url).netloc # Сайт

        self.cache_name = f'{self.path / secrets.token_urlsafe(24)}.mp4' # Название кэша

        # Заголовки HTTP-запросов
        self.headers = {
            # Движок
            'sec-ch-ua': '"Not_A Brand";v="8", '
                f'"Chromium";v="{self.chrome}", '
                f'"Google Chrome";v="{self.chrome}"',
            'sec-ch-ua-mobile': '?0', # Платформа
            'sec-ch-ua-platform': '"Windows"', # ОС
            'upgrade-insecure-requests': '1', # Просьба о защите
            'user-agent': self.User_Agent(), # Имитация браузера Chrome (TLS/HTTP2)
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
            'http_headers': self.headers, # Заголовки HTTP-запросов
            'progress_hooks': [self.Progress_Hook], # Отслеживание прогресса загрузки
            'ffmpeg_location': self.files['ffmpeg'], # Путь ffmpeg
            'outtmpl': self.cache_name, # Путь сохраняемого файла
            'format': 'bestvideo+bestaudio/best', # Качество видео
            'merge_output_format': 'mp4', # Формат после загрузки
            # Принудительная конвертация в .mp4
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'socket_timeout': self.timeout, # Время ожидания ответа от сервера (в секундах)
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
        self.ffprobe_options = {
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

    def User_Agent(self):
        '''Генерация случайного браузера'''
        windows_version = secrets.choice(['11.0; Win64; x64', '10.0; Win64; x64', '10.0'])
        chrome_version = f'{self.chrome}.0.{secrets.choice(range(6778, 6807))}.{secrets.choice(range(85, 110))}'
        user_agent = f'Mozilla/5.0 (Windows NT {windows_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
        return user_agent

    def Convert_Bytes(self, value: int = 0, format: str = '') -> str:
        '''Конвертация байтов'''
        if value is None or value == 0:
            return 'N/A'
        if value < self.factor['KiB']:
            return f'{value} B' + format
        if value < self.factor['MiB']:
            num = value / self.factor['KiB']
            unit = 'KiB'
        elif value < self.factor['GiB']:
            num = value / self.factor['MiB']
            unit = 'MiB'
        else:
            num = value / self.factor['GiB']
            unit = 'GiB'

        if num < 10:
            precision = 3
        elif num < 100:
            precision = 2
        elif num < 1000:
            precision = 1
        else:
            precision = 0
        return f'{num:.{precision}f} {unit}' + format

    def History(self, url: str):
        '''История видео'''
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%B')
        date = now.strftime('%Y.%m.%d')
        time = now.strftime('%H:%M:%S')

        if self.settings['history'] == 1:
            log.info('History recording is enabled.')

            if os.path.exists(self.file_history) and os.path.getsize(self.file_history) > 0:
                with open(self.file_history, 'r', encoding = 'utf-8') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {}

            else:
                data = {}

            year_dict = data.setdefault(year, {})
            month_dict = year_dict.setdefault(month, {})
            day_dict = month_dict.setdefault(date, {})
            day_dict[time] = url

            with open(self.file_history, 'w', encoding = 'utf-8') as file:
                json.dump(data, file, indent = 4, ensure_ascii = False)

        else:
            log.info('History recording is disabled.')

    def File(self):
        '''Создание уникального имени файла'''
        counter = 1
        while True:
            self.final_name = Path(self.path) / f'VID {counter} ({self.site}).mp4'
            if not self.final_name.exists():
                os.rename(self.cache_name, self.final_name)
                break
            counter += 1

    def Progress_Hook(self, data):
        '''Загрузка'''
        if self.cancel_download:
            self.gui.speed.setText('-')
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

            self.gui.progress_bar.setTextVisible(True)
            self.gui.progress_bar.setValue(visual_value)

            self.gui.speed.setText(f'{self.Convert_Bytes(speed, '/s')}')
            self.gui.max_speed.setText(f'{self.Convert_Bytes(self.max_speed, '/s')}')
            self.gui.size.setText(f'{self.Convert_Bytes(volume)}')

        elif data['status'] == 'finished':
            self.gui.progress_bar.setValue(100)
            self.gui.Status('status', 'Download complete, file is being compiled...')

    def Check_Link(self):
        '''Проверка ответа страницы'''
        code = self.response.status_code
        errors = {
            400: 'incorrect request: check the validity of the entered data.',
            401: 'authorization is required: log in to your account to gain access.',
            403: 'access denied: the server rejected your request.',
            404: 'page not found: check the address or it has been deleted.',
            408: 'the timeout period has expired: the server has been waiting for too long.',
            410: 'resource is gone: the requested object has been permanently removed from the server.',
            429: 'too many requests:  you have exceeded the limit, please wait.',
            500: 'internal server error: Something went wrong on the server side.',
            502: 'connection error: the server received an incorrect response from the upstream node.',
            503: 'the server is temporarily unavailable due to technical work or high load.'
        }

        if code in [200, 206]:
            return

        error = errors.get(code, 'Error occurred.')
        full_message = f'Error {code} {error}'

        self.gui.Status('warning', full_message)
        log.error(full_message)

        sys.exit(1)

    def Data(self, url: str):
        '''Получение данных с сайта'''
        try:
            self.Update_Config(url)
            self.response = requests.get(url, impersonate = f'chrome{self.chrome}', timeout = self.timeout)
            self.page = BeautifulSoup(self.response.text, 'html.parser')
            self.Check_Link()

            self.gui.Status('status', 'Getting basic information...')
            log.info('[GETTING BASIC INFORMATION]')

        except requests.exceptions.ConnectionError:
            self.yt_dlp_options = None
            self.gui.Update_Preview(self.files['preview'])

            self.gui.Status('warning', f'Connection error to "{self.domain}". The resource may be blocked and may require a VPN or Proxy.')
            log.error(f'Connection error to "{self.domain}". The resource may be blocked and may require a VPN or Proxy.')
            sys.exit(1)

        except requests.exceptions.Timeout:
            self.yt_dlp_options = None
            self.gui.Update_Preview(self.files['preview'])

            self.gui.Status('warning', f'Exceeded the waiting time for a response from "{self.domain}".')
            log.error(f'Exceeded the waiting time for a response from "{self.domain}".')
            sys.exit(1)

    def Main(self):
        '''Парсинг названий и прямых ссылок'''
        if self.domain == self.sites['Strip2']['domain']:
            raw_title = self.page.find('title').text
            self.title = re.sub(r'\s*[-–—]\s*Strip2.co\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site = next((name for name, info in self.sites.items() if info['domain'] == self.domain), None)

            links = []
            self.video_url = self.page.find_all('a', href = True)
            for link in self.video_url:
                if 'vps402.strip2.co.mp4' in link['href']:
                    links.append(link['href'])

            for _, href in enumerate(links):
                find_link = str(href)
                if find_link and f'/x{len(links) - 1}/' in find_link:
                    self.video_url = find_link

        elif self.domain == self.sites['XGroovy']['domain']:
            raw_title = self.page.find('title').text
            self.title = raw_title
            self.site = next((name for name, info in self.sites.items() if info['domain'] == self.domain), None)

            tags = ['4k', '1080p', '720p', '480p', '240p']
            for tag in tags:
                video = self.page.find('source', title = tag)
                if video:
                    self.video_url = video.get('src')
                    break

        elif self.domain == self.sites['AnalMedia']['domain']:
            raw_title = self.page.find('title').text
            self.title = re.sub(r'\s*[-–—]\s*AnalMedia\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            self.site = next((name for name, info in self.sites.items() if info['domain'] == self.domain), None)

            video = self.page.find('video')
            self.video_url = video.find('source')['src']

        else:
            self.gui.Status('warning', 'Downloads are only available from Strip2, XGroovy, AnalMedia.')
            log.error('Downloads are only available from Strip2, XGroovy, AnalMedia.')
            sys.exit(1)

        self.gui.title.setText(self.title)

        log.info(f'| Name: {self.title}')
        log.info(f'| Direct link: {self.video_url}')

    def Preview(self):
        '''Получение превью'''
        key = next((i for i, v in self.sites.items() if v['domain'] == self.domain), None)
        if key:
            match = re.search(self.sites[key]['pattern'], str(self.page))
            if match:
                image = match.group(0)
                link_image = requests.get(image, impersonate = f'chrome{self.chrome}', timeout = self.timeout).content
                with open(self.temp_preview, 'wb') as preview:
                    preview.write(link_image)
                self.gui.Update_Preview(self.temp_preview)

        log.info(f'| Preview: {image}')

    def More_Info(self):
        '''Получение дополнительной информации'''
        self.gui.Status('status', 'Getting additional information...')
        log.info('[GETTING ADDITIONAL INFORMATION]')

        try:
            video_info = ffmpeg.probe(self.video_url, cmd = self.files['ffprobe'],  **self.ffprobe_options)
            video_stream = next((stream for stream in video_info['streams'] if stream['codec_type'] == 'video'), None)

            width = video_stream.get('width', 0)
            height = video_stream.get('height', 0)
            fps = f'{math.ceil(float(Fraction(video_stream.get('avg_frame_rate', 'N/A'))))}'
            raw_duration = video_stream.get('duration')
            duration = str(timedelta(seconds = float(raw_duration))).split('.')[0] if raw_duration else 'N/A'

            self.gui.quality.setText(f'{width}x{height}')
            self.gui.fps.setText(fps)
            self.gui.duration.setText(duration)

            log.info(f'| Quality: {width}x{height}')
            log.info(f'| FPS: {fps}')
            log.info(f'| Duration: {duration}')

            self.gui.Status('status', 'Video is ready to download!')

        except Exception as e:
            self.gui.Status('warning', f'Error reading technical info via ffprobe: {e}')
            log.error(f'Error reading technical info via ffprobe: {e}')

    def Edit_Tags(self):
        '''Редактирование тегов'''
        try:
            tags = MP4(self.final_name)
            tags.delete()
            tags['\xa9nam'] = self.title  # Название
            tags['\xa9cmt'] = 'https://github.com/Dinger-JC/Deubaso-Composifity' # Комментарий
            tags['\xa9ART'] = f'{self.domain}' # Исполнитель
            tags['\xa9day'] = f'{datetime.now().strftime('%Y')}' # Год
            tags['\xa9gen'] = 'Porn' # Жанр
            tags.save()

        except Exception as e:
            log.error(f'Failed to edit mp4 tags: {e}')

    def Download_Video(self):
        '''Скачивание видео'''
        self.cancel_download = False
        if not self.yt_dlp_options or not self.video_url:
            self.gui.Status('warning', 'The link to the video is missing.')
            log.error('The link to the video is missing.')
            sys.exit(1)

        self.gui.Status('status', 'Downloading videos...')
        log.info('[DOWNLOADING VIDEOS]')

        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
                video.download([self.video_url])

            self.File()
            self.Edit_Tags()

            self.gui.speed.setText('-')
            self.gui.Status('status', f'Downloaded in {str(self.final_name).replace('\\', '/')}')
            log.info(f'| Downloaded in {self.final_name}')

        except Exception as e:
            if 'Download aborted' in str(e):
                self.gui.Status('warning', 'Download aborted')
                log.error('Download aborted')

            else:
                self.gui.Status('warning', f'Unexpected error: {e}')
                log.error(e)
                sys.exit(1)

        finally:
            try:
                os.remove(self.temp_preview)

            except Exception:
                pass

    def Stop(self):
        '''Прерывание скачивания'''
        self.cancel_download = True

        # if self.cancel_download == True:
        #     self.gui.stop_button.setText('⏸︎')
        #
        # if self.cancel_download == False:
        #     self.gui.stop_button.setText('■︎')

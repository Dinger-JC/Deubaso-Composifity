# Deubaso Composifity
# Core

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import math
import os
import re
import secrets
import sys
from datetime import timedelta, datetime
from fractions import Fraction
from pathlib import Path
from urllib.parse import urlparse

# Сторонние библиотеки
import ffmpeg
import yt_dlp
from bs4 import BeautifulSoup
from curl_cffi import requests
from io import BytesIO
from mutagen.mp4 import MP4
from PIL import Image
from yt_dlp.utils._utils import _UnsafeExtensionError

# Локальные модули
from config import chrome, factor, files, settings, sites, tags
from logger import Log

log = Log()



class CORE:
    '''Ядро'''
    def __init__(self):
        '''Инициализация'''
        # Прочее
        self.timeout = 30

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
        self.path = None
        self.cache_video_name = None
        self.cache_preview_name = None
        self.yt_dlp_options = None
        self.ffprobe_options = None
        self.response = None
        self.page = None
        self.title = None
        self.video_link = None
        self.site = None
        self.id = None
        self.link_image = None

    def Stop_Download(self):
        '''Прерывание скачивания'''
        self.cancel_download = True

    def Aliases(self, url: str) -> str:
        '''Извлечение ссылки'''
        if not files['data']['videos'].is_file():
            return url

        try:
            with open(files['data']['videos'], encoding = 'utf-8') as file:
                videos = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return url

        if url in videos:
            url = videos[url]
        return url

    def Update_Config(self, url: str):
        '''Обновление конфигурации для каждого видео'''
        self.signal.Status('info', 'Checking...')

        log.info(f'| Link: {url}')

        # Проверка ссылки
        if not url.startswith(('http://', 'https://')):
            self.signal.Update_Preview(files['images']['png']['other']['preview'])

            self.signal.Status('warning', 'Incorrect link.')
            sys.exit(1)

        self.Write_History(url)
        self.domain = urlparse(url).netloc
        self.date = datetime.now().strftime('%Y.%m.%d')

        # Директория
        self.path = Path(settings['path'])
        self.path.mkdir(parents = True, exist_ok = True)
        self.cache_video_name = f'{self.path / secrets.token_urlsafe(24)}.mp4'
        self.cache_preview_name = f'{self.path / secrets.token_urlsafe(24)}.png'

        # Заголовки HTTP-запросов
        headers = {
            # Движок
            'sec-ch-ua': '"Not_A Brand";v="8", '
                f'"Chromium";v="{chrome}", '
                f'"Google Chrome";v="{chrome}"',
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
            'socket_timeout': self.timeout, # Время ожидания ответа от сервера (в секундах)
            'sleep_interval': 0, # Минимальная случайная пауза между загрузками (в секундах)
            'max_sleep_interval': 2, # Максимальная случайная пауза между запросами (в секундах)
            'retries': 5, # Количество попыток переподключения при ошибке загрузки файла
            'fragment_retries': 5, # Количество попыток загрузки каждого отдельного фрагмента видео
            'rm_cached_metadata': True, # Очистка метаданных из кэша перед началом загрузки
            'nocheckcertificate': True, # Игнорирование ошибок проверки SSL-сертификатов
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
            'tls_verify': '0', # Проверка SSL-сертификатов
            'reconnect': '1', # Автоматическое переподключение
            'seekable': '0', # Чтение потока
            'reconnect_streamed': '1' # Автоматическое переподключение для стримов
        }

    def Generate_User_Agent(self) -> str:
        '''Генерация случайного браузера'''
        windows_version = secrets.choice(['11.0; Win64; x64', '10.0; Win64; x64', '10.0'])
        chrome_version = f'{chrome}.0.{secrets.choice(range(6778, 6807))}.{secrets.choice(range(85, 110))}'
        user_agent = f'Mozilla/5.0 (Windows NT {windows_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
        return user_agent

    def Write_History(self, url: str):
        '''Запись в историю'''
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%B')
        date = now.strftime('%Y.%m.%d')
        time = now.strftime('%H:%M:%S')

        if settings['history'] == 1:
            if files['data']['history'].is_file() and files['data']['history'].stat().st_size > 0:
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
            self.signal.speed.setText('-')
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

            self.signal.progress_bar.setTextVisible(True)
            self.signal.progress_bar.setValue(visual_value)

            self.signal.speed.setText(f'{self.Convert_Bytes(speed, '/s')}')
            self.signal.max_speed.setText(f'{self.Convert_Bytes(self.max_speed, '/s')}')
            self.signal.size.setText(f'{self.Convert_Bytes(volume)}')

        elif data['status'] == 'finished':
            self.signal.progress_bar.setValue(100)
            self.signal.Status('info', 'File is being compiled...')

    def Check_Link(self):
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
            return

        full_message = f'Error {code}. {errors.get(code, '?')}'
        self.signal.Update_Preview(files['images']['png']['other']['preview'])
        self.signal.Status('error', full_message)
        self.Reset()

        sys.exit(1)

    def Prepare(self, url: str):
        '''Подготовка'''
        try:
            url = self.Aliases(url)
            self.Update_Config(url)
            self.response = requests.get(url, impersonate = f'chrome{chrome}', timeout = self.timeout)
            self.page = BeautifulSoup(self.response.text, 'html.parser')
            self.Check_Link()
            self.signal.Status('info', 'Preparing...')

        except requests.exceptions.ConnectionError:
            self.signal.Update_Preview(files['images']['png']['other']['preview'])
            self.signal.Status('error', f'Connection error to "{self.domain}": resource may be blocked and may require VPN or proxy')
            sys.exit(1)

        except requests.exceptions.Timeout:
            self.signal.Update_Preview(files['images']['png']['other']['preview'])
            self.signal.Status('error', f'Exceeded waiting time for a response from "{self.domain}"')
            sys.exit(1)

    def Get_Video(self) -> tuple:
        '''Парсинг названий и прямых ссылок'''
        raw_title = self.page.find('title').text
        video_link = ''

        if self.domain == sites['strip2']['domain']:
            links = []
            title = re.sub(r'\s*[-–—]\s*Strip2.co\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            found_links = self.page.find_all('a', href = True)

            for link in found_links:
                if 'vps402.strip2.co.mp4' in link['href']:
                    links.append(link['href'])

            for _, href in enumerate(links):
                find_link = str(href)
                if find_link and f'/x{len(links) - 1}/' in find_link:
                    video_link = find_link

        elif self.domain == sites['xgroovy']['domain']:
            title = raw_title

            for tag in tags:
                source = self.page.find('source', title = tag)
                if source:
                    video_link = source.get('src')
                    break

        elif self.domain == sites['analmedia']['domain']:
            title = re.sub(r'\s*[-–—]\s*AnalMedia\s*$', '', raw_title, flags = re.IGNORECASE).strip()
            video_link = self.page.select_one('video source')['src']

        elif self.domain == sites['rule34video']['domain']:
            links = {}
            title = raw_title
            found_links = self.page.find_all('a', class_ = 'tag_item tag_item_download')

            for link in found_links:
                text = link.text.lower()
                url = link.get('href')

                for tag in tags:
                    if tag in text:
                        links[tag] = url
                        break

            for tag in tags:
                if tag in links:
                    video_link = links[tag]
                    break

        else:
            self.signal.Status('warning', 'Downloads are only available from Strip2, XGroovy, AnalMedia, Rule34Video')
            sys.exit(1)

        site = next((name for name, info in sites.items() if info['domain'] == self.domain), None)
        video_id = secrets.token_hex(8)

        self.signal.title.setText(title)

        log.info(f'| Name: {title}')
        log.info(f'| Direct link: {video_link}')

        return title, video_link, site, video_id

    def Get_Preview(self):
        '''Получение превью'''
        try:
            image = None
            pattern = sites[self.site]['pattern']

            if '{tag}' in pattern:
                for tag in tags:
                    match = re.search(pattern.replace('{tag}', re.escape(tag)), str(self.page))
                    if match:
                        image = match.group(0)
                        break

            else:
                image = re.search(pattern, str(self.page)).group(0)

            self.link_image = requests.get(image, impersonate = f'chrome{chrome}', timeout = self.timeout).content

            with Image.open(BytesIO(self.link_image)) as preview:
                preview.save(self.cache_preview_name)

            self.signal.Update_Preview(self.cache_preview_name)

            log.info(f'| Preview: {image}')

        except Exception as e:
            self.signal.Status('warning', f'Error get preview: {e}')

    def Download_Preview(self):
        '''Скачивание превью'''
        if self.link_image == None:
            return

        try:
            final_preview_name = self.path / f'{self.site} - {self.date} [PREVIEW_{self.id}].png'

            image = Image.open(BytesIO(self.link_image))
            image.save(final_preview_name, format = 'PNG')

            self.signal.Status('good', f'Preview downloaded: {str(final_preview_name).replace('\\', '/')}')

        except Exception as e:
            self.signal.Status('warning', f'Error download preview: {e}')

    def Get_Info(self):
        '''Получение дополнительной информации'''
        self.signal.Status('info', 'Getting info...')

        try:
            ffprobe_video_info = ffmpeg.probe(self.video_link, cmd = files['bin']['ffprobe'],  **self.ffprobe_options)

            video_stream = next((stream for stream in ffprobe_video_info['streams'] if stream['codec_type'] == 'video'), None)
            width = video_stream.get('width', 0)
            height = video_stream.get('height', 0)
            fps = f'{math.ceil(float(Fraction(video_stream.get('avg_frame_rate', 'N/A'))))}'
            raw_duration = video_stream.get('duration')
            duration = str(timedelta(seconds = float(raw_duration))).split('.')[0] if raw_duration else 'N/A'

            self.signal.quality.setText(f'{width}x{height}')
            self.signal.fps.setText(fps)
            self.signal.duration.setText(duration)

            log.info(f'| Quality: {width}x{height}')
            log.info(f'| FPS: {fps}')
            log.info(f'| Duration: {duration}')

            self.signal.Status('good', 'Video is ready!')

        except Exception as e:
            self.signal.Status('warning', f'Error get info: {e}')

        finally:
            self.signal.button_download.setEnabled(True)

    def Edit_Tags(self, video_name: str, title: str):
        '''Редактирование тегов'''
        try:
            tags = MP4(video_name)
            tags.delete()
            tags['\xa9nam'] = title  # Название
            tags['\xa9cmt'] = 'https://github.com/Dinger-JC/Deubaso-Composifity' # Комментарий
            tags.save()

        except Exception as e:
            self.signal.Status('error', f'Error edit tags: {e}')

    def Download_Video(self):
        '''Скачивание видео'''
        if self.video_link == None:
            return

        self.cancel_download = False
        self.signal.Status('info', 'Downloading videos...')
        _UnsafeExtensionError._enabled = False

        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
                video.download([self.video_link])

            final_video_name = self.path / f'{self.site} - {self.date} [VIDEO_{self.id}].mp4'
            os.rename(self.cache_video_name, final_video_name)
            self.Edit_Tags(final_video_name, self.title)
            self.signal.speed.setText('-')
            self.signal.Status('good', f'Video downloaded: {str(final_video_name).replace('\\', '/')}')

        except Exception as e:
            if 'Download aborted' in str(e):
                self.signal.Status('warning', 'Download aborted')
            else:
                self.signal.Status('error', f'Error download video: {e}')
                sys.exit(1)

        finally:
            _UnsafeExtensionError._enabled = True

            try:
                os.remove(self.cache_preview_name)

            except Exception:
                pass

            self.Reset()

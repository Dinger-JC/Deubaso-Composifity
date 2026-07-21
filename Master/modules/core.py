# Deubaso Composifity
# Core

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from master import *
from logger import *
log = Log()



class CORE:
    '''Ядро'''
    def __init__(self, files):
        '''Инициализация'''
        # Основное
        self.files = files

        # Настройки
        with open(self.files['settings'], encoding = 'utf-8') as file:
            self.settings = json.load(file)

        # Поддерживаемые сайты
        with open(self.files['sites'], encoding = 'utf-8') as file:
            self.sites = json.load(file)

        # Директория скачиваемых видео
        self.path = Path(self.settings['path'])
        self.path.mkdir(parents = True, exist_ok = True)
        self.temp_preview = self.path / 'preview_temp.jpg'

        # Прочее
        self.chrome = '131'
        self.timeout = 30
        self.factor = {'KiB': 1024, 'MiB': 1024 ** 2, 'GiB': 1024 ** 3}

        # Сброс
        self.max_speed = 0
        self.yt_dlp_options = None
        self.video_url = None
        self.cancel_download = False

        # Проверка записи истории
        if self.settings['history'] == 1:
            log.info('History recording is enabled.')

        else:
            log.info('History recording is disabled.')

    # def Files(self, files: dict):
    #     '''Проверка наличия файлов'''
    #     error = False
    #
    #     for name, path in files.items():
    #         if not path.is_file():
    #             if name == 'ffmpeg' or name == 'ffprobe':
    #                 log.critical(f'The "{path}" file was not found.')
    #                 log.critical('You can download it here: https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45.')
    #                 log.critical('After downloading, move the exe file to the bin folder in the root of the project.')
    #                 error = True
    #
    #             elif name == 'history':
    #                 return
    #
    #             elif name == 'videos':
    #                 log.warning(f'The "{path}" file was not found.')
    #
    #             else:
    #                 log.critical(f'The "{path}" file was not found.')
    #                 error = True
    #
    #     if error:
    #         os._exit(0)

    def Aliases(self, url: str) -> str:
        '''Извлечение ссылки'''
        if not self.files['videos'].is_file():
            return url

        try:
            with open(self.files['videos'], encoding = 'utf-8') as file:
                videos = json.load(file)
            presets = videos
            if url in videos:
                url = presets[url]

        except json.JSONDecodeError:
            log.info(f'The "{self.files['videos']}" file is corrupted or has an incorrect JSON format.')

        return url

    def Update_Config(self, url: str):
        '''Обновление конфигурации для каждого видео'''
        self.gui.Status('info', 'Checking...')

        log.info(f'| Link: {url}')

        # Проверка ссылки
        if not re.search(r'^https?://[\w\.-]+\/.*(video|watch).*', url):
            self.yt_dlp_options = None
            self.gui.Update_Preview(self.files['preview_icon'])

            self.gui.Status('warning', 'Incorrect link. This link could not be found.')
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
            'ffmpeg_location': str(self.files['ffmpeg']), # Путь к ffmpeg
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
            'nocheckcertificate': True, # Игнорирование ошибок проверки SSL-сертификатов
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
            'tls_verify': '0', # Проверка SSL-сертификатов
            'reconnect': '1', # Автоматическое переподключение
            'seekable': '0', # Чтение потока
            'reconnect_streamed': '1' # Автоматическое переподключение для стримов
        }

    def User_Agent(self) -> str:
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
            if self.files['history'].is_file() and self.files['history'].stat().st_size > 0:
                with open(self.files['history'], 'r', encoding = 'utf-8') as file:
                    data = json.load(file)

            else:
                data = {}

            year_dict = data.setdefault(year, {})
            month_dict = year_dict.setdefault(month, {})
            day_dict = month_dict.setdefault(date, {})
            day_dict[time] = url

            with open(self.files['history'], 'w', encoding = 'utf-8') as file:
                json.dump(data, file, indent = 4, ensure_ascii = False)

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

            self.gui.Status('info', 'Download complete, file is being compiled...')

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

        self.gui.Update_Preview(self.files['preview_icon'])
        self.gui.Status('error', full_message)

        sys.exit(1)

    def Get_Data(self, url: str):
        '''Получение данных с сайта'''
        try:
            self.Update_Config(url)
            self.response = requests.get(url, impersonate = f'chrome{self.chrome}', timeout = self.timeout)
            self.page = BeautifulSoup(self.response.text, 'html.parser')
            self.Check_Link()

            self.gui.Status('info', 'Getting basic information...')

        except requests.exceptions.ConnectionError:
            self.yt_dlp_options = None
            self.gui.Update_Preview(self.files['preview_icon'])

            self.gui.Status('error', f'Connection error to "{self.domain}". The resource may be blocked and may require a VPN or Proxy.')
            sys.exit(1)

        except requests.exceptions.Timeout:
            self.yt_dlp_options = None
            self.gui.Update_Preview(self.files['preview_icon'])

            self.gui.Status('error', f'Exceeded the waiting time for a response from "{self.domain}".')
            sys.exit(1)

    def Get_Info(self):
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
            sys.exit(1)

        self.gui.title.setText(self.title)

        log.info(f'| Name: {self.title}')
        log.info(f'| Direct link: {self.video_url}')

    def Get_Preview(self):
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

    def Get_Add_Info(self):
        '''Получение дополнительной информации'''
        self.gui.Status('info', 'Getting additional information...')

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

            self.gui.Status('info', 'Video is ready to download!')

        except Exception as e:
            self.gui.Status('error', f'Error reading technical info via ffprobe: {e}')

    def File_Name(self):
        '''Создание уникального имени файла'''
        date = datetime.now().strftime('%Y.%m.%d')
        counter = 1
        while True:
            self.final_name = self.path / f'{date} {self.site} VID {counter}.mp4'
            if not self.final_name.exists():
                os.rename(self.cache_name, self.final_name)
                break
            counter += 1

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
            self.gui.Status('error', f'Failed to edit mp4 tags: {e}')

    def Download_Video(self):
        '''Скачивание видео'''
        self.cancel_download = False
        if not self.yt_dlp_options or not self.video_url:
            self.gui.Status('error', 'The link to the video is missing.')
            sys.exit(1)

        self.gui.Status('info', 'Downloading videos...')

        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as video:
                video.download([self.video_url])

            self.File_Name()
            self.Edit_Tags()
            self.gui.speed.setText('-')

            self.gui.Status('info', f'Downloaded in {str(self.final_name).replace('\\', '/')}')

        except Exception as e:
            if 'Download aborted' in str(e):
                self.gui.Status('warning', 'Download aborted')

            else:
                self.gui.Status('error', f'Unexpected error: {e}')
                sys.exit(1)

        finally:
            try:
                os.remove(self.temp_preview)

            except Exception:
                pass

    def Stop_Download(self):
        '''Прерывание скачивания'''
        self.cancel_download = True

# Deubaso Composifity
# Config

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
from pathlib import Path



# Файлы
project = Path(__file__).resolve().parent.parent
files = {
    # Папка bin
    'ffmpeg_e': project / 'bin' / 'ffmpeg.exe',
    'ffprobe_e': project / 'bin' / 'ffprobe.exe',
    # Папка config
    'settings_j': project / 'config' / 'settings.json',
    'sites_j': project / 'config' / 'sites.json',
    # Папка data
    'history_j': project / 'data' / 'history.json',
    'videos_j': project / 'data' / 'videos.json',
    # Папка images/png
    'download_i': project / 'images' / 'png' / 'download.png',
    'link_i': project / 'images' / 'png' / 'link.png',
    'logo_i': project / 'images' / 'png' / 'logo.png',
    'preview_i': project / 'images' / 'png' / 'preview.png',
    'settings_i': project / 'images' / 'png' / 'settings.png',
    'stop_i': project / 'images' / 'png' / 'stop.png',
    # Папка images/social
    'github_i': project / 'images' / 'social' / 'github.png',
    'telegram_i': project / 'images' / 'social' / 'telegram.png',
    'tiktok_i': project / 'images' / 'social' / 'tiktok.png',
    # Папка images/svg
    'download_s': project / 'images' / 'svg' / 'download.svg',
    'link_s': project / 'images' / 'svg' / 'link.svg',
    'preview_s': project / 'images' / 'svg' / 'preview.svg',
    'settings_s': project / 'images' / 'svg' / 'settings.svg',
    'stop_s': project / 'images' / 'svg' / 'stop.svg',
    # Папка modules
    'config_p': project / 'modules' / 'config.py',
    'core_p': project / 'modules' / 'core.py',
    'logger_p': project / 'modules' / 'logger.py',
    'master_window_p': project / 'modules' / 'master_window.py',
    'presets_p': project / 'modules' / 'presets.py',
    'settings_p': project / 'modules' / 'settings.py',
}

# Основное
name = 'Deubaso Composifity'
version = '2026.07.25.2b'
size_window = [1000, 600]
border_radius_small = 10
border_radius_big = 15
font_family = 'GungsuhW33-Regular'
font_big = 18
font_small = 14

# Цвета
colors = {
    # Задний фон
    'main_start': 'rgba(7, 17, 37, 1)',
    'main_end': 'rgba(14, 32, 65, 1)',
    # Текст
    'text': 'rgba(255, 255, 255, 1)',
    'sub_text': 'rgba(180, 180, 180, 1)',
    # Градиенты
    'info': 'rgba(15, 20, 39, 1)',
    'stroke': 'rgba(0, 0, 0, 0)',
    'fill': 'rgba(255, 255, 255, 0.15)',
    'hover_stroke': 'rgba(1, 179, 189, 1)',
    'hover_fill': 'rgba(0, 67, 112, 0.5)',
    'hover_start': 'rgba(99, 146, 234, 1)',
    'hover_end': 'rgba(2, 219, 172, 1)',
    'hover_start_pressed': 'rgba(99, 146, 234, 0.4)',
    'hover_end_pressed': 'rgba(2, 219, 172, 0.4)',
    # Статусы
    'warning': 'rgba(255, 193, 62, 1)',
    'error': 'rgba(227, 88, 111, 1)'
}
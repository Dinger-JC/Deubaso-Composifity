# Deubaso Composifity
# Initialization

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import os
import sys
from pathlib import Path

os.system('')

# Локальные модули
try:
    from config import files
    from core import CORE
    from logger import Log
    from master_window import MASTER_WINDOW
    from presets import *

    log = Log()

except ImportError as e:
    print(f'\033[91mCould not import modules: \033[7;91m{e.name}\033[0m')
    print(f'Make sure dependencies are installed: \033[4mpip install -r requirements.txt\033[0m')
    sys.exit(1)



def Files():
    '''Проверка наличия файлов'''
    error = False
    items = list(files.items())

    while items:
        name, value = items.pop()

        if isinstance(value, dict):
            items.extend(value.items())
            continue

        if value.is_file():
            continue

        if name in ('ffmpeg', 'ffprobe'):
            print(f'\033[7;91m"{value}"\033[91m not found\033[0m')
            print(f'\033[93mYou can download it here: \033[3;91mhttps://github.com/GyanD/codexffmpeg/releases/tag/9.0.1.\033[0m')
            print(f'After downloading, move exe file to bin folder in root of project')
            error = True

        elif name == 'videos':
            print(f'\033[7;93m"{value}"\033[93m not found\033[0m')

        else:
            print(f'\033[7;91m"{value}"\033[91m not found\033[0m')
            error = True

    if error:
        sys.exit(1)



if __name__ == '__main__':
    Files()

    try:
        log.info('Start')

        # Приложение
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(True)

        # Инициализация шрифта
        font_id = QFontDatabase.addApplicationFont(str(files['config']['font']))
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))

        # Защита от повторного запуска
        lock = QLockFile(str(Path(sys.argv[0]).resolve().with_name('app.lock')))
        lock.setStaleLockTime(10000)
        if not lock.tryLock(100):
            QMessageBox.warning(None, 'Warning', 'App is already running!')
            sys.exit(0)

        # Структура
        core = CORE()
        master_window = MASTER_WINDOW(core)
        core.signal = master_window

        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')

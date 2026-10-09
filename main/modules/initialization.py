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
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'content'))

# Локальные модули
try:
    from config import files, project
    from core import CORE
    from logger import Log
    from main import MAIN
    from presets import *

    log = Log()

except ImportError as e:
    print(f'\033[91mCould not import modules: \033[7;91m{e.name}\033[0m')
    print(f'Make sure dependencies are installed: \033[4mpip install -r requirements.txt\033[0m')
    sys.exit(1)



def Checking_Files():
    '''Проверка файлов'''
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
            print(f'Not found \033[7;91m"{value}"\033[0;91m')
            print(f'\033[93mYou can download it here: \033[3;91mhttps://github.com/GyanD/codexffmpeg/releases/tag/9.0.1.\033[0m')
            print(f'After downloading, move exe file to bin folder in root of project')
            error = True

        elif name == 'videos':
            print(f'Not found \033[7;93m"{value}"\033[0;93m')

        else:
            print(f'Not found \033[7;91m"{value}"\033[0;91m')
            error = True

    if error:
        sys.exit(1)



if __name__ == '__main__':
    Checking_Files()
    log.info('Start')

    try:
        # Приложение
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(True)

        # Основной шрифт
        font_id = QFontDatabase.addApplicationFont(str(files['content']['font']))
        if font_id != -1:
            app.setFont(QFont(QFontDatabase.applicationFontFamilies(font_id)[0]))

        # Шрифт логов
        font_logs_id = QFontDatabase.addApplicationFont(str(files['content']['font_logs']))
        if font_logs_id != -1:
            files['content']['font_logs'] = QFontDatabase.applicationFontFamilies(font_logs_id)[0]

        # Защита от повторного запуска
        lock = QLockFile(str(project / 'app.lock'))
        lock.setStaleLockTime(10000)
        if not lock.tryLock(100):
            QMessageBox.warning(None, 'Warning', 'App is already running!')
            sys.exit(0)

        # Структура
        core = CORE()
        main = MAIN(core)
        core.signal = main

        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')

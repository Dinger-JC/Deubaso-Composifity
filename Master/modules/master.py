# Parser Deubaso Composifity
# Master initialization

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
try:
    from master_window import *
    from logger import Log
    log = Log(__name__)

except ImportError:
    print('Could not import local modules.')
    sys.exit(1)



if __name__ == '__main__':
    try:
        log.info('Start')
        app = QApplication(sys.argv)

        core = CORE()
        master = MASTER(core, '2026.07.20.0b')
        core.gui = master

        master.window.show()
        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')

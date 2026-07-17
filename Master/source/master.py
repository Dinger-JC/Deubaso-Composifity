# Parser Deubaso Composifity
# Master initialization

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
try:
    from core import *
    from master_window import *
    from logger import Log
    log = Log(__name__)

except ImportError:
    print("Couldn't import local modules.")
    sys.exit(1)



if __name__ == '__main__':
    try:
        log.info('Start')
        app = QApplication(sys.argv)

        core = CORE()
        master = MASTER(core = core)
        core.gui = master

        master.window.show()
        sys.exit(app.exec())

    except Exception as e:
        log.error(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')

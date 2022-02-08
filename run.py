from tk_main import TkMain

import getpass
USER_NAME = getpass.getuser()


def add_to_startup(file_path=""):
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


def start_application():
    TkMain()


if __name__ == '__main__':
    start_application()

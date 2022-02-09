import getpass
import yaml

from tk_main import TkMain, Config


def add_to_startup(file_path=""):
    USER_NAME = getpass.getuser()
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


def start_application():
    f = open("config.yaml", "r")
    yaml_dic = yaml.safe_load(f)
    f.close()
    config = Config(yaml_dic)
    TkMain(config)


if __name__ == '__main__':
    start_application()

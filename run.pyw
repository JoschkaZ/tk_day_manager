import os
import yaml

from tk_main import TkMain, Config


def start_application():
    file_path = os.path.abspath(__file__)
    f = open(os.sep.join(file_path.split(os.sep)[:-1] + ["config.yaml"]), "r")
    yaml_dic = yaml.safe_load(f)
    f.close()
    config = Config(yaml_dic)
    TkMain(config)


if __name__ == '__main__':
    start_application()

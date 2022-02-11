import getpass
import os

user_name = getpass.getuser()

bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % user_name
bat_path = bat_path + '\\' + "tk_day_manager.bat"
file_path = os.path.abspath(__file__)
file_path = os.sep.join(file_path.split(os.sep)[:-1] + ['run.pyw'])

with open(bat_path, "w+") as bat_file:
    bat_command = f"start pythonw {file_path}"
    bat_file.write(bat_command)
    print(f"wrote '{bat_command}' to '{bat_path}'")

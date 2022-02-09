import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import threading
import pyttsx3
from datetime import date
from csv import writer
import pickle as pkl
import os
from win32api import GetSystemMetrics
import time
import yaml

from tk_main.config import Config
from tk_main.helper import Helper


class PomodoroGui:

    def __init__(self):
        f = open("config.yaml", "r")
        yaml_dic = yaml.safe_load(f)
        f.close()

        self._config = Config(yaml_dic)
        self._helper = Helper(self._config)
        self.times = [
            '5',
            '10',
            '20',
            '30',
            '45',
            '60',
            '120'
        ]

        self.state = 0
        self.time_to_go = 0
        self.job_time = 0
        self.aborted = False
        self.killed = False

        # class instances
        self.root = None
        self.speech_engine = pyttsx3.init()

        # widgets
        self.button = None
        self.button_start = None
        self.str_job = None
        self.entry_job = None
        self.str_time = None
        self.combobox_time = None
        self.label_time = None

        self.t = threading.Thread(target=self.timer)
        self.t.start()

        self.build_tk()

    def build_tk(self):
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.8)
        self.root.overrideredirect(1)
        self.root.focus_force()
        self.root.attributes("-topmost", True)
        if GetSystemMetrics(0) == 2560:
            self.root.geometry("267x50+2289+1005")
        else:
            self.root.geometry("267x50+1650+700")

        # close button
        self.button = Button(master=self.root, text='Close', command=self.quit)
        self.button.grid(row=0, column=4, sticky=W + E + N + S)

        # button start
        self.button_start = Button(master=self.root, text='Start', command=self.start)
        self.button_start.grid(row=1, column=4, sticky=W + E + N + S)

        # job entry
        self.str_job = StringVar()
        self.entry_job = tk.Entry(self.root, textvariable=self.str_job)
        self.entry_job.grid(column=2, row=0, columnspan=2, sticky=N + E + S + W)

        # combobox for selecting time span
        self.str_time = StringVar()
        self.combobox_time = Combobox(master=self.root,
                                      textvar=self.str_time,
                                      values=self.times)
        self.combobox_time.set('20')
        self.combobox_time.grid(row=1, column=3, columnspan=1, sticky=W+E+N+S)

        # label1
        self.label_time = Label(text='00:00', font='Helvetica 24 bold')
        self.label_time.grid(row=0, column=0, rowspan=2)

        self.root.grid_rowconfigure(0, weight=1, uniform='x')
        self.root.grid_rowconfigure(1, weight=1, uniform='x')

        self.root.grid_columnconfigure(0, weight=30, uniform='y')
        self.root.grid_columnconfigure(1, weight=1, uniform='y')
        self.root.grid_columnconfigure(2, weight=20, uniform='y')
        self.root.grid_columnconfigure(3, weight=20, uniform='y')
        self.root.grid_columnconfigure(4, weight=20, uniform='y')

        self.root.mainloop()

    def quit(self):
        self.killed = True
        time.sleep(1.1)
        self.root.destroy()

    def start(self):
        str_time = self.str_time.get()
        self.job_time = float(str_time)
        str_job = self.str_job.get()
        if self.state == 0:  # not yet running
            if str_time != '' and str_job != '':
                self.time_to_go = float(str_time) * 60.

                self.entry_job["state"] = DISABLED
                self.combobox_time["state"] = DISABLED

                self.state = 1
                self.button_start.configure(text='Stop')
                self.say(str_time + ' minute session started for job: '+ str_job)

        elif self.state == 1:
            self.button_start.configure(text='Start')
            self.entry_job["state"] = NORMAL
            self.combobox_time["state"] = NORMAL

            self.state = 0
            self.aborted = True
            self.time_to_go = 0

            self.say('session interrupted')

    def timer(self):
        while True:
            print(self.killed)
            if self.killed:
                break
            time.sleep(1)
            if self.time_to_go > 0 or self.aborted == True:
                self.time_to_go = max(0, self.time_to_go-1)

                if self.label_time is not None:
                    minutes = str(int(self.time_to_go/60))
                    seconds = str(int(self.time_to_go % 60))
                    if len(minutes) == 1:
                        minutes = '0'+minutes
                    if len(seconds) == 1:
                        seconds = '0'+seconds
                    self.label_time.configure(text=minutes+':'+seconds)

                if self.time_to_go == 0:  # pomodoro finished

                    if self.aborted:
                        self.aborted = False
                    else:  # proper finish
                        self.say('Session finished! Congratulations!')

                        with open(r'C:\\DATA\\POMODORO\\'+str(date.today())+'.csv', 'a+', newline='') as write_obj:
                            csv_writer = writer(write_obj)
                            csv_writer.writerow([str(time.time()), self.str_time.get(), self.str_job.get()])

                        self.increment()

                    self.state = 0
                    self.entry_job["state"] = NORMAL
                    self.combobox_time["state"] = NORMAL
                    self.button_start.configure(text='Start')
                    self.combobox_time.set('20')
                    self.str_job.set('')

    def say(self, s):
        self.speech_engine.say(s)
        self.speech_engine.runAndWait()

    def increment(self):
        fn = r'C:\\DATA\\VBLM\\pomodoro_counts.pkl'

        if os.path.isfile(fn):
            success = False
            while not success:
                try:
                    infile = open(fn, 'rb')
                    pdic = pkl.load(infile)
                    infile.close()

                    today = self._helper.get_date_str()
                    if today in pdic:
                        pdic[today] += float(self.job_time) / 20
                    else:
                        pdic[today] = float(self.job_time) / 20
                    outfile = open(fn, 'wb')
                    pkl.dump(pdic, outfile)
                    outfile.close()
                    success = True
                except:
                    print('opening pickle failed. trying again...')
                    time.sleep(1)
        else:
            outfile = open(fn, 'wb')
            pkl.dump({self._helper.get_date_str(): 1}, outfile)
            outfile.close()

import tkinter as tk
from tkinter import ttk
import time
import pyttsx3
from win32api import GetSystemMetrics

from .frames import FrameMain
from .data import Data


class TkMain:

    def __init__(self):
        self.speech_engine = pyttsx3.init()

        self.data = Data()

        self.root = tk.Tk()
        self.last_tab_change_timestamp = 0

        self.tab_control = ttk.Notebook(self.root)
        self.tab_1 = ttk.Frame(self.tab_control)
        self.tab_2 = ttk.Frame(self.tab_control)
        self.tab_3 = ttk.Frame(self.tab_control)

        self.frame_main = FrameMain(self.tab_1, self.data)

        self.last_tab_change = 0

        self.build_tk()

    def build_tk(self):
        # configure root
        self.root.attributes("-alpha", 0.8)
        self.root.overrideredirect(1)
        self.root.focus_force()
        self.root.attributes("-topmost", True)
        if GetSystemMetrics(0) == 2560:
            self.root.geometry("267x337+2287+1058")
        else:
            self.root.geometry("267x337+1650+700")
        self.root.configure(bg='black')

        # set up tabs
        self.tab_control.bind("<<NotebookTabChanged>>", self.tab_changed)
        self.tab_control.add(self.tab_1, text='Main')
        self.tab_control.add(self.tab_2, text='Food')
        self.tab_control.add(self.tab_3, text='Stats')
        self.tab_control.pack(expand=1, fill="both")


        # start thread and main loop
        self.thread_auto()
        self.root.mainloop()

    def tab_changed(self, evt):
        self.last_tab_change = time.time()
        print(self.tab_control.tab(self.tab_control.select(), 'text'))

    def thread_auto(self):

        # check if focus should be changed back to main tab
        if self.tab_control.tab(self.tab_control.select(), 'text') != 'Main':
            if time.time() - self.last_tab_change > 60:
                self.tab_control.select(self.tab_1)

        # GET CURRENT TIME
        now = time.strftime("%H:%M:%S").split(':')
        print(now)
        now = int(now[0]) * 3600 + int(now[1]) * 60 + int(now[2])

        '''
        # UPDATE PROGRESS BARS & LABELS ON MAIN FRAME
        p1state = max(min(time_passed / (self.data.wake_sleep_times[1] - self.data.wake_sleep_times[0])*100, 100), 0)
        p2state = self.data.scores['main_calories']
        p3state = self.data.scores['main_water']
        p4state = self.data.scores['main_work']
        p5state = self.data.scores['main_sleep']
        p6state = self.data.scores['main_sports']
        self.frame_main.main_progressbars.progressbar_tod_var.set(max(min(p1state, 100), 0))
        self.frame_main.main_progressbars.progressbar_kcal_var.set(max(min(p2state, 100), 0))
        self.frame_main.main_progressbars.progressbar_water_var.set(max(min(p3state, 100), 0))
        self.frame_main.main_progressbars.progressbar_work_var.set(max(min(p4state, 100), 0))
        self.frame_main.main_progressbars.progressbar_sleep_var.set(max(min(p5state, 100), 0))
        self.frame_main.main_progressbars.progressbar_sport_var.set(max(min(p6state, 100), 0))
        self.frame_main.main_progressbars.lv1['text'] = str(int(np.round(p1state, 0))) + '%'
        self.frame_main.main_progressbars.lv2['text'] = str(int(np.round(p2state, 0))) + '%'
        self.frame_main.main_progressbars.lv3['text'] = str(int(np.round(p3state, 0))) + '%'
        self.frame_main.main_progressbars.lv4['text'] = str(int(np.round(p4state, 0))) + '%'
        self.frame_main.main_progressbars.lv5['text'] = str(int(np.round(p5state, 0))) + '%'
        self.frame_main.main_progressbars.lv6['text'] = str(int(np.round(p6state, 0))) + '%'
        '''

        self.root.after(1000, self.thread_auto)

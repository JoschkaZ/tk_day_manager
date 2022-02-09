import tkinter as tk
from tkinter import ttk
import time
import pyttsx3
from win32api import GetSystemMetrics
import numpy as np

from .frames import FrameMain
from .data import Data
from .config import Config
from ._static import *

class TkMain:

    def __init__(self, config: Config):
        self._root = tk.Tk()
        self._config = config
        self._data = Data(self._config, self._root)
        self._speech_engine = pyttsx3.init()

        self._last_tab_change_timestamp = 0

        self._tab_control = ttk.Notebook(self._root)
        self._tab_1 = ttk.Frame(self._tab_control)
        self._tab_2 = ttk.Frame(self._tab_control)
        self._tab_3 = ttk.Frame(self._tab_control)

        self._frame_main = FrameMain(self._tab_1, self._data, self._config)

        self._last_tab_change = 0

        self._build_tk()

    def _build_tk(self):
        # configure root
        self._root.attributes("-alpha", 0.8)
        self._root.overrideredirect(1)
        self._root.focus_force()
        self._root.attributes("-topmost", True)
        if GetSystemMetrics(0) == 2560:
            self._root.geometry("267x337+2289+1059")
        else:
            self._root.geometry("267x337+1650+700")
        self._root.configure(bg='black')

        # set up tabs
        self._tab_control.bind("<<NotebookTabChanged>>", self.tab_changed)
        self._tab_control.add(self._tab_1, text='Main')
        self._tab_control.add(self._tab_2, text='Food')
        self._tab_control.add(self._tab_3, text='Stats')
        self._tab_control.pack(expand=1, fill="both")

        # start thread and main loop
        self.thread_auto()
        self._root.mainloop()

    def tab_changed(self, _):
        self._last_tab_change = time.time()

    def thread_auto(self):

        # check if focus should be changed back to main tab
        if self._tab_control.tab(self._tab_control.select(), 'text') != 'Main':
            if time.time() - self._last_tab_change > 3:
                self._tab_control.select(self._tab_1)

        # update time and scores of data
        self._data.update_time()
        self._data._update_scores()
        seconds_of_day = self._data.get_seconds_of_day()

        # update progress bars and labels
        progressbar_variables = self._data.get_progressbar_variables()
        scores = self._data.get_scores()
        dynamic_labels = self._frame_main.get_progress_bars_dynamic_labels()
        for i, progressbar_name in enumerate(PROGRESSBAR_NAME_DIC):
            score_name = PROGRESSBAR_NAME_DIC[progressbar_name]
            capped_score = max(min(scores[score_name], 100), 0)
            progressbar_variables[i].set(capped_score)
            dynamic_labels[i]['text'] = str(int(np.round(capped_score, 0))) + '%'

        # update main score label
        todays_score_main_label = self._frame_main.get_todays_score_main_label()
        todays_score_main_label['text'] = f'Score: ' + str(np.round(scores['total'], 2))

        # check if there is eomthing to say
        timed_messages_read = self._data.get_timed_message_read()
        for i, timed_message in enumerate(self._config.timed_messages()):
            if not timed_messages_read[i]:
                if np.abs(timed_message.seconds_of_day() - seconds_of_day) < 10:
                    self._speech_engine.say(timed_message.text())
                    self._speech_engine.runAndWait()
                    timed_messages_read[i] = True

        # set time left
        time_left = np.max([self._config.go_to_bed_seconds_of_day() - seconds_of_day, 0])
        hours = str(int(time_left / 3600))
        minutes = str(int((time_left % 3600) / 60))
        seconds = str(int(time_left % 60))
        if len(hours) == 1:
            hours = '0' + hours
        if len(minutes) == 1:
            minutes = '0' + minutes
        if len(seconds) == 1:
            seconds = '0' + seconds
        time_left_label = self._frame_main.get_time_left_label()
        time_left_label['text'] = (hours + ':' + minutes + ':' + seconds)

        # check if to send to background or foreground
        to_background_until = self._frame_main.get_to_background_until()
        if to_background_until > time.time():
            self._frame_main.set_background_button_color('red')
            self._root.attributes("-topmost", False)
        else:
            self._frame_main.set_background_button_color('green')
            self._root.attributes("-topmost", True)

        print('...')
        self._root.after(500, self.thread_auto)

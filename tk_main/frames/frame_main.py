from tkinter import *
import tkinter as tk
import time
import os
import threading

from .frame_checkboxes import FrameCheckboxes
from .frame_progress_bars import FrameProgressBars
from .frame_time_left import FrameTimeLeft
from .frame_todays_score import FrameTodaysScore
from .frame_duration_input import FrameDurationInput
from ..data import Data
from ..config import Config


class FrameMain:
    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._config = config

        self._to_background_until = 0

        self._frame_left = tk.Frame(self._parent, borderwidth=0)
        self._frame_right = tk.Frame(self._parent, borderwidth=0)

        self._frame_buttons_ = tk.Frame(self._frame_right, borderwidth=2, relief='sunken')
        self._button_background = tk.Button(master=self._frame_buttons_, text='M', command=self._send_form_to_back)
        self._button_pomodoro = tk.Button(master=self._frame_buttons_, text='P', command=self._start_pomodoro_process)

        self._frame_progress_bars_ = tk.Frame(self._frame_left, borderwidth=2, relief='sunken')
        self._frame_progress_bars = FrameProgressBars(self._frame_progress_bars_, self._data, self._config)

        self._frame_checkboxes_ = tk.Frame(self._frame_right, borderwidth=2, relief='sunken')
        self._frame_checkboxes = FrameCheckboxes(self._frame_checkboxes_, self._data, self._config)

        self._frame_time_left_ = tk.Frame(self._frame_left, borderwidth=2, relief='sunken')
        self._frame_time_left = FrameTimeLeft(self._frame_time_left_, self._data, self._config)

        self._frame_todays_score_ = tk.Frame(self._frame_left, borderwidth=2, relief='sunken')
        self._frame_todays_score = FrameTodaysScore(self._frame_todays_score_, self._data, self._config)

        self._frame_duration_input_ = tk.Frame(self._frame_right, borderwidth=2, relief='sunken')
        self._frame_duration_input = FrameDurationInput(self._frame_duration_input_, self._data, self._config)

        self._configure_grid()
        self.set_background_button_color('green')

    def _configure_grid(self):

        # parent
        self._frame_left.grid(row=0, column=0, sticky=W + N + S + E)
        self._frame_right.grid(row=0, column=1, sticky=W + N + S + E)
        # set row and column weights
        self._parent.grid_rowconfigure(0, weight=1, uniform='x')
        self._parent.grid_columnconfigure(0, weight=1, uniform='y')
        self._parent.grid_columnconfigure(1, weight=1, uniform='y')

        # left frame
        self._frame_time_left_.grid(row=0, column=0, sticky=W + N + S + E)
        self._frame_todays_score_.grid(row=1, column=0, sticky=W + N + S + E)
        self._frame_progress_bars_.grid(row=2, column=0, sticky=W + N + S + E)
        self._frame_left.grid_rowconfigure(0, weight=10, uniform='x2')
        self._frame_left.grid_rowconfigure(1, weight=30, uniform='x2')
        self._frame_left.grid_rowconfigure(2, weight=60, uniform='x2')
        self._frame_left.grid_columnconfigure(0, weight=1, uniform='y2')

        # right frame
        self._frame_buttons_.grid(row=0, column=0, sticky=W + N + S + E)
        self._frame_checkboxes_.grid(row=1, column=0, sticky=W + N + S + E)
        self._frame_duration_input_.grid(row=2, column=0, sticky=W + N + S + E)
        self._frame_right.grid_rowconfigure(0, weight=10, uniform='x3')
        self._frame_right.grid_rowconfigure(1, weight=70, uniform='x3')
        self._frame_right.grid_rowconfigure(2, weight=15, uniform='x3')
        self._frame_right.grid_columnconfigure(0, weight=1, uniform='y3')

        # frame buttons
        self._button_background.grid(row=0, column=0, sticky=W + N + S + E)
        self._button_pomodoro.grid(row=0, column=2, sticky=W + N + S + E)
        self._frame_buttons_.grid_columnconfigure(0, weight=100, uniform='y')
        self._frame_buttons_.grid_columnconfigure(1, weight=100, uniform='y')
        self._frame_buttons_.grid_columnconfigure(2, weight=100, uniform='y')

    def _send_form_to_back(self):
        if self._to_background_until > time.time():
            self._to_background_until = 0
        else:
            self._to_background_until = time.time() + 20 * 60

    def get_progress_bars_dynamic_labels(self):
        return self._frame_progress_bars.get_dynamic_labels()

    def get_todays_score_main_label(self):
        return self._frame_todays_score.get_main_score_label()

    def get_time_left_label(self):
        return self._frame_time_left.get_time_left_label()

    def get_to_background_until(self):
        return self._to_background_until

    def set_background_button_color(self, color):
        self._button_background.configure(bg=color)

    def update_duration_labels(self):
        self._frame_duration_input.update_labels()

    def update_plot(self):
        self._frame_todays_score.update_plot()

    @staticmethod
    def _start_pomodoro_process():

        def worker():
            print('thread started')
            path = os.path.abspath(__file__)
            path = os.sep.join(path.split(os.sep)[:-3] + ['start_pomodoro_gui.py'])
            os.system(f'python {path}')
            print('thread killed')
        threading.Thread(target=worker).start()

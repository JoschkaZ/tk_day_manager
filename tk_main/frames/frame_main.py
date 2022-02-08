from tkinter import *
import tkinter as tk
import time

from .frame_checkboxes import FrameCheckboxes
from .frame_progress_bars import FrameProgressBars
from .frame_time_left import FrameTimeLeft
from .frame_todays_score import FrameTodaysScore
import os
import threading


class FrameMain:
    def __init__(self, parent, data):
        self._parent = parent
        self._data = data

        self._frame_menu_ = tk.Frame(self._parent, borderwidth=2, relief='sunken')
        self._button_background = tk.Button(master=self._frame_menu_, text='M', command=self._send_form_to_back)
        self._button_pomodoro = tk.Button(master=self._frame_menu_, text='P', command=FrameMain._start_pomodoro_process)

        self._frame_progress_bars_ = tk.Frame(self._parent, borderwidth=2, relief='sunken')
        self._frame_progress_bars = FrameProgressBars(self._frame_progress_bars_, self._data)

        self._frame_checkboxes_ = tk.Frame(self._parent, borderwidth=2, relief='sunken')
        self._frame_checkboxes = FrameCheckboxes(self._frame_checkboxes_, self._data)

        self._frame_time_left_ = tk.Frame(self._parent, borderwidth=2, relief='sunken')
        self._frame_time_left = FrameTimeLeft(self._frame_time_left_, self._data)

        self._frame_todays_score_ = tk.Frame(self._parent, borderwidth=2, relief='sunken')
        self._frame_todays_score = FrameTodaysScore(self._frame_todays_score_, self._data)

        self._configure_grid()

    def _configure_grid(self):
        # configure frame_menu contents
        self._button_background.grid(row=0, column=0, sticky=W + N + S + E)
        self._button_pomodoro.grid(row=0, column=2, sticky=W + N + S + E)
        self._frame_menu_.grid_columnconfigure(0, weight=100, uniform='y')
        self._frame_menu_.grid_columnconfigure(1, weight=100, uniform='y')
        self._frame_menu_.grid_columnconfigure(2, weight=100, uniform='y')

        # configure all frames
        self._frame_time_left_.grid(row=1, rowspan=1, column=1, sticky=W + N + S + E)
        self._frame_todays_score_.grid(row=2, rowspan=1, column=1, sticky=W + N + S + E)
        self._frame_progress_bars_.grid(row=3, column=1, sticky=W + N + S + E)
        self._frame_menu_.grid(row=1, column=2, sticky=W+N+S+E)
        self._frame_checkboxes_.grid(row=2, column=2, sticky=W + N + S + E, rowspan=2)

        # set row and column weights
        self._parent.grid_rowconfigure(0, weight=5, uniform='x')
        self._parent.grid_rowconfigure(1, weight=25, uniform='x')
        self._parent.grid_rowconfigure(2, weight=100, uniform='x')
        self._parent.grid_rowconfigure(3, weight=100, uniform='x')
        self._parent.grid_rowconfigure(5, weight=5, uniform='x')
        self._parent.grid_columnconfigure(0, weight=5, uniform='y')
        self._parent.grid_columnconfigure(1, weight=100, uniform='y')
        self._parent.grid_columnconfigure(2, weight=100, uniform='y')
        self._parent.grid_columnconfigure(5, weight=5, uniform='y')

    def _send_form_to_back(self):
        if time.time() - self._data.to_background_time < 30 * 60:
            self._data.to_background_time = 0
        else:
            self._data.to_background_time = time.time()

    @staticmethod
    def _start_pomodoro_process():
        def worker():
            print('thread started')
            os.system(r'python C:\coding\code_archive\LM3\pomodoro.py')
            print('thread killed')
        threading.Thread(target=worker).start()

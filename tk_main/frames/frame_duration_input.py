from tkinter import *
import tkinter as tk
import tkinter.font as tk_font


from ..data import Data
from ..config import Config


class FrameDurationInput:

    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._config = config

        font_style = tk_font.Font(family="Lucida Grande", size=8)
        self._work_label = tk.Label(self._parent, text='---', font=font_style)
        self._sport_label = tk.Label(self._parent, text='---', font=font_style)

        self._spinbox_work_minutes = Spinbox(self._parent, from_=0, to=600)
        self._spinbox_exercise_minutes = Spinbox(self._parent, from_=0, to=600)

        self._button_work_add = tk.Button(master=self._parent, text='+', command=self._add_work)
        self._button_work_subtract = tk.Button(master=self._parent, text='-', command=self._subtract_work)
        self._button_exercise_add = tk.Button(master=self._parent, text='+', command=self._add_exercise)
        self._button_exercise_subtract = tk.Button(master=self._parent, text='-', command=self._subtract_exercise)

        self._configure_grid()

    def _configure_grid(self):
        self._spinbox_work_minutes.grid(row=0, column=1, sticky=N+E+S+W)
        self._spinbox_exercise_minutes.grid(row=1, column=1, sticky=N+E+S+W)
        self._work_label.grid(row=0, column=0, sticky=N+S+W)
        self._sport_label.grid(row=1, column=0, sticky=N+S+W)

        self._button_work_add.grid(row=0, column=2, sticky=N+E+S+W)
        self._button_work_subtract.grid(row=0, column=3, sticky=N+E+S+W)
        self._button_exercise_add.grid(row=1, column=2, sticky=N+E+S+W)
        self._button_exercise_subtract.grid(row=1, column=3, sticky=N+E+S+W)

        self._parent.grid_rowconfigure(0, weight=100, uniform='x')
        self._parent.grid_rowconfigure(1, weight=100, uniform='x')
        self._parent.grid_columnconfigure(0, weight=40, uniform='y')
        self._parent.grid_columnconfigure(1, weight=30, uniform='y')
        self._parent.grid_columnconfigure(2, weight=15, uniform='y')
        self._parent.grid_columnconfigure(3, weight=15, uniform='y')

    def _add_work(self):
        self._data.get_scores()['pomodoro_minutes'] += float(self._spinbox_work_minutes.get())
        self._spinbox_work_minutes.delete(0, "end")
        self._spinbox_work_minutes.insert(0, 0)
        self._data.need_to_update_scores = True

    def _subtract_work(self):
        self._data.get_scores()['pomodoro_minutes'] = \
            max(0, self._data.get_scores()['pomodoro_minutes'] - float(self._spinbox_work_minutes.get()))
        self._spinbox_work_minutes.delete(0, "end")
        self._spinbox_work_minutes.insert(0, 0)
        self._data.need_to_update_scores = True

    def _add_exercise(self):
        self._data.get_scores()['exercise_minutes'] += float(self._spinbox_exercise_minutes.get())
        self._spinbox_exercise_minutes.delete(0, "end")
        self._spinbox_exercise_minutes.insert(0, 0)
        self._data.need_to_update_scores = True

    def _subtract_exercise(self):
        self._data.get_scores()['exercise_minutes'] = \
            max(0, self._data.get_scores()['exercise_minutes'] - float(self._spinbox_exercise_minutes.get()))
        self._spinbox_exercise_minutes.delete(0, "end")
        self._spinbox_exercise_minutes.insert(0, 0)
        self._data.need_to_update_scores = True

    def update_labels(self):
        scores = self._data.get_scores()
        date_int = self._data.get_date_int()
        pomodoro_dic = self._data.get_pomodoro_dic()
        pomodoro_minutes = 0
        if date_int in pomodoro_dic:
            pomodoro_minutes = pomodoro_dic[date_int]

        work_minutes = scores['pomodoro_minutes'] + pomodoro_minutes
        exercise_minutes = scores['exercise_minutes']
        self._work_label['text'] = f"W: {int(work_minutes)}m"
        self._sport_label['text'] = f"S: {int(exercise_minutes)}m"

from tkinter import *
import tkinter as tk
import tkinter.font as tk_font

from ..data import Data
from ..config import Config


class FrameTimeLeft:

    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._config = config

        font_style = tk_font.Font(family="Lucida Grande", size=12)
        self._time_left_label = tk.Label(self._parent, text='---', font=font_style)
        self._time_left_label.grid(row=0, column=0, sticky=W + N + S + E)
        self._parent.grid_rowconfigure(0, weight=100, uniform='x')
        self._parent.grid_columnconfigure(0, weight=100, uniform='y')

    def get_time_left_label(self):
        return self._time_left_label

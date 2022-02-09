from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.font as tk_font

from ..data import Data
from ..config import Config
from .._static import *


class FrameProgressBars:

    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._config = config

        # static labels
        font_style = tk_font.Font(family="Lucida Grande", size=8)
        static_labels = [tk.Label(self._parent, text=progressbar_name, font=font_style)
                         for progressbar_name in PROGRESSBAR_NAME_DIC.keys()]

        # progressbars
        self._progressbars = [Progressbar(self._parent, orient=HORIZONTAL, length=1000, mode='determinate',
                                          variable=progressbar_variable)
                              for progressbar_variable in self._data.get_progressbar_variables()]

        # dynamic labels
        self._dynamic_labels = [tk.Label(self._parent, text=progressbar_name, font=font_style)
                                for progressbar_name in PROGRESSBAR_NAME_DIC.keys()]

        # set row and column positions
        for i, static_label in enumerate(static_labels):
            static_label.grid(row=i*2, column=0, sticky=W+N+S)

        for i, progressbar in enumerate(self._progressbars):
            progressbar.grid(row=i*2, column=1, sticky=W + N + S, columnspan=1)

        for i, dynamic_label in enumerate(self._dynamic_labels):
            dynamic_label.grid(row=i*2, column=2, sticky=W + N + S)

        # set row and column weights
        for i, _ in enumerate(PROGRESSBAR_NAME_DIC.keys()):
            self._parent.grid_rowconfigure(i*2, weight=100, uniform='x')
            self._parent.grid_rowconfigure(i*2+1, weight=25, uniform='x')
        #self._parent.grid_rowconfigure(100, weight=200, uniform='x')

        self._parent.grid_columnconfigure(0, weight=50, uniform='y')
        self._parent.grid_columnconfigure(1, weight=90, uniform='y')
        self._parent.grid_columnconfigure(2, weight=50, uniform='y')

    def get_dynamic_labels(self):
        return self._dynamic_labels

from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.font as tk_font


class FrameProgressBars:

    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self._build()

    def _build(self):
        # static labels
        font_style = tk_font.Font(family="Lucida Grande", size=8)
        l1 = tk.Label(self.parent, text='Time ', font=font_style)
        l2 = tk.Label(self.parent, text='kcal ', font=font_style)
        l3 = tk.Label(self.parent, text='Water', font=font_style)
        l4 = tk.Label(self.parent, text='Work', font=font_style)
        l5 = tk.Label(self.parent, text='Sleep', font=font_style)
        l6 = tk.Label(self.parent, text='Sport', font=font_style)

        # progressbars
        self.progressbar_tod_var = DoubleVar()
        self.progressbar_tod = Progressbar(self.parent,
                                           orient=HORIZONTAL, length=1000, mode='determinate',
                                           variable=self.progressbar_tod_var)
        self.progressbar_kcal_var = DoubleVar()
        self.progressbar_kcal = Progressbar(self.parent,
                                            orient=HORIZONTAL, length=1000, mode='determinate',
                                            variable=self.progressbar_kcal_var)
        self.progressbar_water_var = DoubleVar()
        self.progressbar_water = Progressbar(self.parent,
                                             orient=HORIZONTAL, length=1000, mode='determinate',
                                             variable=self.progressbar_water_var)
        self.progressbar_work_var = DoubleVar()
        self.progressbar_work = Progressbar(self.parent,
                                            orient=HORIZONTAL, length=1000, mode='determinate',
                                            variable=self.progressbar_work_var)
        self.progressbar_sleep_var = DoubleVar()
        self.progressbar_sleep = Progressbar(self.parent,
                                             orient=HORIZONTAL, length=1000, mode='determinate',
                                             variable=self.progressbar_sleep_var)
        self.progressbar_sport_var = DoubleVar()
        self.progressbar_sport = Progressbar(self.parent,
                                             orient=HORIZONTAL, length=1000, mode='determinate',
                                             variable=self.progressbar_sport_var)

        # dynamic labels
        self.lv1 = tk.Label(self.parent, text='Time ', font=font_style)
        self.lv2 = tk.Label(self.parent, text='kcal ', font=font_style)
        self.lv3 = tk.Label(self.parent, text='Water', font=font_style)
        self.lv4 = tk.Label(self.parent, text='Work', font=font_style)
        self.lv5 = tk.Label(self.parent, text='Sleep', font=font_style)
        self.lv6 = tk.Label(self.parent, text='Sport', font=font_style)

        # set row and column positions
        l1.grid(row=0, column=0, sticky=W+N+S)
        l4.grid(row=1, column=0, sticky=W + N + S)
        l6.grid(row=2, column=0, sticky=W + N + S)
        l2.grid(row=3, column=0, sticky=W+N+S)
        l3.grid(row=4, column=0, sticky=W+N+S)
        l5.grid(row=5, column=0, sticky=W + N + S)

        self.progressbar_tod.grid(row=0, column=1, sticky=W + N + S, columnspan=1)
        self.progressbar_work.grid(row=1, column=1, sticky=W + N + S, columnspan=1)
        self.progressbar_sport.grid(row=2, column=1, sticky=W + N + S, columnspan=1)
        self.progressbar_kcal.grid(row=3, column=1, sticky=W + N + S, columnspan=1)
        self.progressbar_water.grid(row=4, column=1, sticky=W + N + S, columnspan=1)
        self.progressbar_sleep.grid(row=5, column=1, sticky=W + N + S, columnspan=1)

        self.lv1.grid(row=0, column=2, sticky=W + N + S)
        self.lv4.grid(row=1, column=2, sticky=W + N + S)
        self.lv6.grid(row=2, column=2, sticky=W + N + S)
        self.lv2.grid(row=3, column=2, sticky=W + N + S)
        self.lv3.grid(row=4, column=2, sticky=W + N + S)
        self.lv5.grid(row=5, column=2, sticky=W + N + S)

        # set row and column weights
        self.parent.grid_rowconfigure(0, weight=100, uniform='x')
        self.parent.grid_rowconfigure(1, weight=100, uniform='x')
        self.parent.grid_rowconfigure(2, weight=100, uniform='x')
        self.parent.grid_rowconfigure(3, weight=100, uniform='x')
        self.parent.grid_rowconfigure(4, weight=100, uniform='x')
        self.parent.grid_rowconfigure(5, weight=100, uniform='x')
        self.parent.grid_rowconfigure(100, weight=300, uniform='x')

        self.parent.grid_columnconfigure(0, weight=50, uniform='y')
        self.parent.grid_columnconfigure(1, weight=100, uniform='y')
        self.parent.grid_columnconfigure(2, weight=50, uniform='y')

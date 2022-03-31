from tkinter import *
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from ..data import Data
from ..config import Config


class FrameTodaysScore:

    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._config = config

        # figure
        frame_macros = tk.Frame(self._parent, bg='blue', width=10, height=10)
        figure_macros = plt.Figure()
        self.canvas_macros = FigureCanvasTkAgg(figure_macros, master=frame_macros)
        cvw_left = self.canvas_macros.get_tk_widget()
        cvw_left.pack(expand=True, fill='both')
        self.ax_scores = figure_macros.add_subplot(1, 1, 1)
        self.ax_scores.plot([0, 1, 2], [0, 1, 3], alpha=1, color='black', linewidth=1)
        figure_macros.tight_layout()
        self.ax_scores.get_xaxis().set_visible(False)
        self.ax_scores.get_yaxis().set_visible(False)

        self._main_score_label = tk.Label(self._parent, text='Score: --.-%')

        self._main_score_label.grid(row=0, column=0, sticky=N+E+S+W)
        frame_macros.grid(row=1, column=0, sticky=N+E+S+W)

        self._parent.grid_rowconfigure(0, weight=20, uniform='x')
        self._parent.grid_rowconfigure(1, weight=80, uniform='x')
        self._parent.grid_columnconfigure(0, weight=100, uniform='y')

    def update_plot(self):
        print('p', end='')
        scores = self._data.get_scores()
        current_score = scores['total']

        self.ax_scores.clear()
        self.ax_scores.axhline(current_score, color='red', linestyle='-', alpha=0.7)
        self.ax_scores.plot(self._data.get_total_score_emas(), color='black')
        total_scores = self._data.get_total_scores()
        self.ax_scores.scatter(range(len(total_scores)), total_scores, color='black', alpha=0.5, marker='.')
        ax = self.canvas_macros.figure.axes[0]
        ax.axis('off')

        y_lim_max = max(100, current_score) * 1.05
        y = 0
        while y < y_lim_max:
            ax.axhline(y, color='black', alpha=0.3)
            y += 20

        ax.set_ylim(0, y_lim_max)
        ax.grid()
        self.canvas_macros.draw()

    def get_main_score_label(self):
        return self._main_score_label

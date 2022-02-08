from tkinter import *
import tkinter as tk


class FrameTimeLeft:

    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self._build()

    def _build(self):
        self.l1 = tk.Label(self.parent, text='Time ')
        self.l1.grid(row=0, column=0, sticky=W + N + S)
        self.parent.grid_rowconfigure(0, weight=100, uniform='x')
        self.parent.grid_columnconfigure(0, weight=100, uniform='y')

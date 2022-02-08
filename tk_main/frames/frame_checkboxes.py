from tkinter import *
from tkinter.ttk import *

from ..config import HABIT_CHECKLIST
from ..data import Data


class FrameCheckboxes:

    def __init__(self, parent, data: Data):
        self._parent = parent
        self._data = data
        self._checkbox_values = {}

        for habit in HABIT_CHECKLIST:
            self._checkbox_values[habit[0]] = IntVar()

        # set initial checkbox values
        checkbox_df = self._data.get_checkbox_df()
        if checkbox_df is not None:
            for check_name in self._checkbox_values:
                self._checkbox_values[check_name].set(checkbox_df[checkbox_df.name == check_name].value.values[0])
        self._build()

    def _build(self):
        check_buttons = []
        for habit in HABIT_CHECKLIST:
            habit_name = habit[0]
            check_buttons.append(
                Checkbutton(self._parent, text=habit_name, variable=self._checkbox_values[habit_name],
                            command=self._checkbox_change)
            )
        for i, check_button in enumerate(check_buttons):
            check_button.grid(row=i+1, column=1, sticky=W+N+S+E)

    def _checkbox_change(self):
        self._data.update_checkbox_df(self._checkbox_values)

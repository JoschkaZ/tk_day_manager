from tkinter import *
from tkinter.ttk import *

from ..config import Config
from ..data import Data


class FrameCheckboxes:

    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._config = config

        check_buttons = []
        checkbox_variable_dic = self._data.get_checkbox_variable_dic()
        for habit in self._config.habits():
            check_buttons.append(
                Checkbutton(self._parent, text=habit.name(), variable=checkbox_variable_dic[habit.name()],
                            command=self._data.update_checkbox_df)
            )
        for i, check_button in enumerate(check_buttons):
            check_button.grid(row=i+1, column=1, sticky=W+N+S+E)

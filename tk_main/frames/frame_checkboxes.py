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
            check_button.grid(row=i, column=1, sticky=W+N+S+E)

        self._sequence_check_buttons = []
        for habit in self._config.sequence_habits():
            self._sequence_check_buttons.append(
                Checkbutton(self._parent, text=habit.name(), variable=checkbox_variable_dic[habit.name()],
                            command=self._sequence_button_press)
            )
        for i, check_button in enumerate(self._sequence_check_buttons):
            check_button.grid(row=len(check_buttons)+i, column=1, sticky=W+N+S+E)

        for i in range(len(check_buttons) + len(self._sequence_check_buttons)):
            self._parent.grid_rowconfigure(i, weight=10, uniform='x')

        self._sequence_button_press()

    def _sequence_button_press(self):
        checkbox_variable_dic = self._data.get_checkbox_variable_dic()

        earlier_unchecked = False
        is_next = False
        for i, habit in enumerate(self._config.sequence_habits()):
            check = checkbox_variable_dic[habit.name()].get()
            if not earlier_unchecked and check == 0:
                earlier_unchecked = True
                self._sequence_check_buttons[i].config(state=NORMAL)
            else:
                if earlier_unchecked and not is_next:
                    # set to zero and disable
                    checkbox_variable_dic[habit.name()].set(0)
                    self._sequence_check_buttons[i].config(state=DISABLED)
                    print('did')
        self._data.update_checkbox_df()
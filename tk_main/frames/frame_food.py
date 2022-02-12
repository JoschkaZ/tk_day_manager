import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import *
from tkinter.ttk import *
import numpy as np
import time

from ..helper import Helper
from ..data import Data
from ..config import Config


class FrameFood:
    def __init__(self, parent, data: Data, config: Config):
        self._parent = parent
        self._data = data
        self._helper = Helper(config)

        self._FOOD_NAMES = self._data.get_food_names()
        self._FOOD_DF = self._data.get_foods_df()

        self._button_add = Button(master=self._parent, text='Confirm', command=self._button_press)
        self._button_delete = Button(master=self._parent, text='Delete', command=self._delete_item)
        self._scale = tk.Scale(master=self._parent, from_=0, to=1, orient=HORIZONTAL, command=self.scale_changed,
                               resolution=1)
        self._scrollbar = Scrollbar(self._parent)
        self._listbox = Listbox(self._parent, yscrollcommand=self._scrollbar.set)
        self._button_reload = Button(self._parent, text='R', command=self._button_reload)

        self._combobox_var = StringVar()
        self._combobox = AutocompleteCombobox(master=self._parent,
                                              textvar=self._combobox_var,
                                              completevalues=self._FOOD_NAMES)
        self._selected_food_dic = None
        self._build()

    def _button_reload(self):
        self._data.reload_foods_df()
        self._FOOD_NAMES = self._data.get_food_names()
        self._FOOD_DF = self._data.get_foods_df()
        self._combobox.configure(completevalues=self._FOOD_NAMES)

    def _build(self):
        self._combobox_var.trace('w', self._combobox_changed)
        self._combobox.set('')
        self._combobox.grid(row=0, column=0, columnspan=2, sticky=W+E+N+S)
        self._button_reload.grid(row=0, column=2, sticky=W + E + N + S)

        self._button_add.grid(row=1, column=0, sticky=W + E + N + S)
        self._button_delete.grid(row=1, column=1, columnspan=2, sticky=W + E + N + S)

        self._scale.grid(row=2, column=0, columnspan=2, sticky=W + E + N + S)

        self._scrollbar.grid(row=3, column=2, sticky=W+N+S)
        self._listbox.bind('<<ListboxSelect>>', self._listbox_selection_changed)
        self._listbox.grid(row=3, column=0, columnspan=2, sticky=W+E+N+S)
        self._scrollbar.config(command=self._listbox.yview)

        self._parent.grid_rowconfigure(0, weight=1, uniform='x')
        self._parent.grid_rowconfigure(1, weight=1, uniform='x')
        self._parent.grid_rowconfigure(2, weight=2, uniform='x')
        self._parent.grid_rowconfigure(3, weight=10, uniform='x')
        self._parent.grid_columnconfigure(0, weight=10, uniform='y')
        self._parent.grid_columnconfigure(1, weight=8, uniform='y')
        self._parent.grid_columnconfigure(2, weight=2, uniform='y')

        self._button_add['state'] = 'disabled'
        self._button_delete['state'] = 'disabled'

        self._update_listbox()

    def _button_press(self):
        if self._combobox.get() in self._FOOD_NAMES:  # valid entry
            self._button_add['state'] = 'disabled'
            self._button_delete['state'] = 'disabled'
            self._data.add_to_food_hist(timestamp=time.time(),
                                        food_name=self._combobox.get(),
                                        food_qty=self._scale.get())
            self._update_listbox()
            self._combobox.set('')
            self._scale.config(from_=1)
            self._scale.config(to=2)
            self._scale.config(resolution=1)
            self._scale.set(1)
        else:
            print('Invalid')

    def _combobox_changed(self, index, value, op):
        temp = self._combobox.get()
        if self._button_add is not None:
            if temp in self._FOOD_NAMES:
                if self._button_add['state'] != 'enabled':
                    self._button_add['state'] = 'enabled'

        if temp in self._FOOD_NAMES:  # set scale
            self._selected_food_dic = self._FOOD_DF[self._FOOD_DF['name'] == temp].to_dict(orient='records')
            assert len(self._selected_food_dic) == 1
            self._selected_food_dic = self._selected_food_dic[0]

            # selected_unit = self._selected_food_dic['scale_unit'].values[0]
            for i in range(2):
                self._scale.config(from_=self._selected_food_dic['scale_min'])
                self._scale.config(to=self._selected_food_dic['scale_max'])
                self._scale.config(resolution=self._selected_food_dic['scale_step'])
                self._scale.set(self._selected_food_dic['scale_default'])

    def _update_listbox(self):
        self._listbox.delete(0, tk.END)
        food_hist_df = self._data.get_food_hist_df()
        if food_hist_df is not None:
            for line in food_hist_df.values:
                self._listbox.insert(END, f"{int(line['timestamp'])} \t {line['qty']} \t {line['name']}")
        self._data.need_to_update_scores = True

    def _delete_item(self):
        self._button_delete['state'] = 'disabled'
        sel_idx = self._listbox.curselection()[0]
        food_hist_df = self._data.get_food_hist_df()

        self._data.remove_from_food_hist(food_hist_df.index[sel_idx])
        self._update_listbox()

    def _listbox_selection_changed(self, _):
        if self._button_delete['state'] != 'enabled':
            self._button_delete['state'] = 'enabled'

    def scale_changed(self, _):
        current_value = self._scale.get()
        selected_step_scale = self._selected_food_dic['scale_step']
        new_value = np.round(current_value / selected_step_scale) * selected_step_scale
        if new_value != current_value:
            self._scale.set(new_value)

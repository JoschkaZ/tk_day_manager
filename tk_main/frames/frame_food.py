import tkinter as tk # Python 3
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import *
from tkinter.ttk import *
from helper import *
import numpy as np
import csv

class Frame_food():
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data

        self.button = None

        # helpers
        self.food_names = list(self.data.df_foods['food'].values)

    def build(self):

        # combobox
        self.v = StringVar()
        self.v.trace('w', self.combobox_changed)
        self.combobox = AutocompleteCombobox(master=self.parent,
                                             textvar=self.v,
                                             completevalues=self.food_names)
        self.combobox.set('')
        self.combobox.grid(row=0, column=0, columnspan=2, sticky=W+E+N+S)

        # button confirm
        self.button = Button(master=self.parent, text='Confirm', command=self.button_press)
        self.button.grid(row=1, column=0, sticky=W + E + N + S)
        # button delete
        self.button_delete = Button(master=self.parent, text='Delete', command=self.delete_item)
        self.button_delete.grid(row=1, column=1, sticky=W + E + N + S)
        # scale
        self.scale = tk.Scale(master=self.parent, from_=0, to=1, orient=HORIZONTAL, command=self.scale_changed,
                           resolution=1)
        self.scale.grid(row=2, column=0, columnspan=2, sticky=W + E + N + S)

        # scrollbar & listbox
        scrollbar = Scrollbar(self.parent)
        scrollbar.grid(row=3, column=2, sticky=W+N+S)
        self.listbox = Listbox(self.parent, yscrollcommand=scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.listbox_selection_changed)
        self.listbox.grid(row=3, column=0, columnspan=2, sticky=W+E+N+S)
        scrollbar.config(command=self.listbox.yview)

        self.parent.grid_rowconfigure(0, weight=1, uniform='x')
        self.parent.grid_rowconfigure(1, weight=1, uniform='x')
        self.parent.grid_rowconfigure(2, weight=2, uniform='x')
        self.parent.grid_rowconfigure(3, weight=10, uniform='x')
        self.parent.grid_columnconfigure(0, weight=1, uniform='y')
        self.parent.grid_columnconfigure(1, weight=1, uniform='y')

        self.button['state'] = 'disabled'
        self.button_delete['state'] = 'disabled'

        self.update_listbox()

    def button_press(self):
        if self.combobox.get() in self.food_names:  # valid entry
            self.button['state'] = 'disabled'
            self.button_delete['state'] = 'disabled'
            self.data.add_to_food_hist(date=get_date_int(),
                                         food_name=self.combobox.get(),
                                         food_qty=self.scale.get())
            self.update_listbox()
            self.combobox.set('')

            self.scale.config(from_=1)
            self.scale.config(to=2)
            self.scale.config(resolution=1)
            self.scale.set(1)

        else:  # invalid entry
            print('Invalid')

    def combobox_changed(self, index, value, op):
        temp = self.combobox.get()
        if self.button is not None:
            if temp in self.food_names:
                if self.button['state'] != 'enabled':
                    self.button['state'] = 'enabled'

        if temp in self.food_names: # set scale
            sunit = self.data.df_foods[self.data.df_foods['food'] == temp]['unit'].values[0]
            sfrom = self.data.df_foods[self.data.df_foods['food'] == temp]['min_scale'].values[0]
            sto = self.data.df_foods[self.data.df_foods['food'] == temp]['max_scale'].values[0]
            sdefault = self.data.df_foods[self.data.df_foods['food'] == temp]['default_scale'].values[0]
            self.sscale = self.data.df_foods[self.data.df_foods['food'] == temp]['step_scale'].values[0]
            for i in range(2):
                self.scale.config(from_=sfrom)
                self.scale.config(to=sto)
                self.scale.config(resolution=self.sscale)
                self.scale.set(sdefault)


    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        if self.data.df_food_hist is not None:
            print(self.data.df_food_hist.head())

            todays_entries = self.data.df_food_hist[self.data.df_food_hist['date'] == get_date_int()].values
            print(todays_entries)
            print(get_date_int())
            for line in todays_entries:
                self.listbox.insert(END, str('  '.join([str(x) for x in line])))

    def delete_item(self):
        self.button_delete['state'] = 'disabled'
        try:
            sel_idx = self.listbox.curselection()[0]
        except:
            return
        todays_entries = self.data.df_food_hist[self.data.df_food_hist['date'] == get_date_int()].index
        print(self.data.df_food_hist)
        print(todays_entries)

        self.data.remove_from_food_hist(todays_entries[sel_idx])
        self.update_listbox()


    def listbox_selection_changed(self, evt):
        if self.button_delete['state'] != 'enabled':
            self.button_delete['state'] = 'enabled'

    def scale_changed(self, evt):
        current = self.scale.get()
        newvalue = np.round(current / self.sscale) * self.sscale
        if newvalue != current:
            self.scale.set(newvalue)
            print(newvalue)


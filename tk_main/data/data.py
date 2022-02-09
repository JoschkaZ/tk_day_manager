import pandas as pd
import os
from tkinter import IntVar, DoubleVar

from ..helper import Helper
from ..config import Config
from .._static import *


class Data:

    def __init__(self, config: Config, parent):
        self._parent = parent
        self._config = config
        self._helper = Helper(self._config)
        self._foods_df = None
        self._food_hist_df = None
        self._checkbox_df = None
        self._scores_hist_df = None

        self._scores = {'pomodoro_minutes': 0.,
                        'exercise_minutes': 0.}
        self._todays_macros = {}

        self._seconds_of_day = 0
        self._date_str = ''

        # init timed message was set
        self._timed_message_read = [False for _ in self._config.timed_messages()]

        # init dataframes
        self.update_time(is_init=True)
        self._read_dataframes()

        # init checkbox variables
        self._checkbox_variable_dic = {}
        for habit in self._config.habits():
            self._checkbox_variable_dic[habit.name()] = IntVar()

        if self._checkbox_df is not None:
            for check_name in self._checkbox_variable_dic:
                self._checkbox_variable_dic[check_name].set(
                    self._checkbox_df[self._checkbox_df.name == check_name].value.values[0])

        # init progressbar variables
        self._progressbar_variables = [DoubleVar() for _ in PROGRESSBAR_NAME_DIC.keys()]

        # update scores
        self._update_scores()

    def update_time(self, is_init=False):
        date_str = self._helper.get_date_str()
        self._seconds_of_day = self._helper.get_seconds_of_day()
        if date_str != self._date_str and not is_init:
            self._timed_message_read = [False for _ in self._config.timed_messages()]
            self._dump_dataframes()
            self._read_dataframes()
            self._update_scores()
        self._date_str = date_str

    def _read_dataframes(self):
        data_path = self._config.data_path()

        # foods
        file_path = os.sep.join([data_path, 'Foods.csv'])
        self._foods_df = pd.read_csv(file_path)
        self._foods_df['food'] = self._foods_df['food'].apply(lambda x: x.replace(' ', '_'))

        # today's food hist
        file_path = os.sep.join([data_path, 'food_hists', self._date_str + '.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._food_hist_df = pd.read_csv(file_path)
        else:
            self._food_hist_df = None

        # today's checkbox hist
        file_path = os.sep.join([data_path, 'checkbox_hists', self._date_str + '.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._checkbox_df = pd.read_csv(file_path)
        else:
            self._checkbox_df = None

        # score hist
        file_path = os.sep.join([data_path, 'scores_hist.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._scores_hist_df = pd.read_csv(file_path)
        else:
            self._scores_hist_df = None

    def _dump_dataframes(self):
        self._dump_foods_df()
        self._dump_food_hist_df()
        self._dump_checkbox_df()
        self._dump_scores_hist_df()

    def _dump_foods_df(self):
        if self._foods_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'Foods.csv'])
            self._foods_df.to_csv(file_path)

    def _dump_food_hist_df(self):
        if self._food_hist_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'food_hists', self._date_str + '.csv'])
            self._food_hist_df.to_csv(file_path)

    def _dump_checkbox_df(self):
        if self._checkbox_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'checkbox_hists', self._date_str + '.csv'])
            self._checkbox_df.to_csv(file_path)

    def _dump_scores_hist_df(self):
        if self._scores_hist_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'scores_hist.csv'])
            self._scores_hist_df.to_csv(file_path)

    def _update_scores(self):
        # compute 'time score'
        self._scores['time'] = max(
            min((self.get_seconds_of_day() - self._config.get_up_seconds_of_day())
                / (self._config.go_to_bed_seconds_of_day() - self._config.get_up_seconds_of_day()) * 100, 100), 0)

        # compute today's macros
        self._todays_macros = {}
        macros = ['kcal', 'carb', 'fat', 'protein', 'water']
        for macro in macros:
            self._todays_macros[macro] = 0

        if self._food_hist_df is not None:

            for food_hist_row in self._food_hist_df.to_dict(orient="records"):
                food_name = food_hist_row['food']
                food_q = food_hist_row['qty']
                for macro in macros:
                    self._todays_macros[macro] += float(food_q) * float(
                        self._foods_df[self._foods_df['food'] == food_name][macro].values[0])

        # penalize if going over [0,100]
        self._scores['kcal'] = max(0, 1 - abs(self._todays_macros['kcal'] / self._config.kcal_target() - 1)) * 100
        # flat at max [0,100]
        self._scores['water'] = min(1, self._todays_macros['water'] / self._config.water_target()) * 100
        # flat at max [0,100]
        self._scores['protein'] = min(1, self._todays_macros['protein'] / self._config.protein_target()) * 100
        # start dropping over max [0,100]
        self._scores['carb'] = max(0, 1 - max(0, self._todays_macros['carb'] / self._config.carb_target() - 1)) * 100
        # flat at max [0,100]
        self._scores['fat'] = min(1, self._todays_macros['fat'] / self._config.fat_target()) * 100

        # weighted linear combination of sub scores [0,100]
        self._scores['main_macros'] = (self._scores['kcal'] * 2.
                                       + self._scores['water'] * 3.
                                       + self._scores['protein']
                                       + self._scores['carb']
                                       + self._scores['fat']) / 8 * 1.2

        self._scores['main_work'] = min(1.5, self._scores['pomodoro_minutes']
                                        / self._config.pomodoro_minutes_target()) * 100
        self._scores['main_sports'] = min(1.2, self._scores['exercise_minutes']
                                          / self._config.exercise_minutes_target()) * 100

        # compute habit score
        self._scores['main_habits'] = 0
        if self._checkbox_df is not None:
            temp = 0
            for habit in self._config.habits():
                checkbox_state = self._checkbox_df[self._checkbox_df['name'] == habit.name()]['value'].values[0]
                self._scores['main_habits'] += checkbox_state * habit.weight()
                temp += habit.weight()
            self._scores['main_habits'] /= temp / 100

        self._scores['total'] = (self._scores['main_work'] * 1 +
                                 self._scores['main_sports'] * 1 +
                                 self._scores['main_macros'] * 1 +
                                 self._scores['main_habits'] * 1) / 4

        self.do_update_stats = True

        # update and dump score hist df
        date = self._helper.get_date_str()
        self._scores['date'] = date
        df_new = pd.DataFrame(self._scores, index=[0])

        if self._scores_hist_df is None:
            self._scores_hist_df = df_new
        else:
            self._scores_hist_df = self._scores_hist_df[self._scores_hist_df['date'] != date]
            self._scores_hist_df = pd.concat([self._scores_hist_df, df_new], axis=0, ignore_index=True)

        self._dump_scores_hist_df()

    def add_to_food_hist(self, timestamp, food_name, food_qty):
        df_new = pd.DataFrame([[timestamp, food_name, food_qty]], columns=['timestamp', 'food', 'qty'])
        if self._food_hist_df is None:
            self._food_hist_df = df_new
        else:
            self._food_hist_df = pd.concat([self._food_hist_df, df_new], axis=0, ignore_index=True)
        self._dump_food_hist_df()
        #self._update_scores()

    def remove_from_food_hist(self, index):
        self._food_hist_df.drop(index, inplace=True)
        self._food_hist_df.reset_index(inplace=True, drop=True)
        self._dump_food_hist_df()
        #self._update_scores()

    def update_checkbox_df(self):
        check_names = []
        check_values = []
        for check in self._checkbox_variable_dic:
            val = self._checkbox_variable_dic[check].get()
            check_names.append(check)
            check_values.append(val)
        self._checkbox_df = pd.DataFrame({'name': check_names, 'value': check_values})
        self._dump_checkbox_df()
        #self._update_scores()

    def get_checkbox_df(self):
        return self._checkbox_df

    def get_checkbox_variable_dic(self):
        return self._checkbox_variable_dic

    def get_seconds_of_day(self):
        return self._seconds_of_day

    def get_scores(self):
        return self._scores

    def get_date_str(self):
        return self._date_str

    def get_progressbar_variables(self):
        return self._progressbar_variables

    def get_timed_message_read(self):
        return self._timed_message_read

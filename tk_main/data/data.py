import pandas as pd
import os
from tkinter import IntVar, DoubleVar
import time
import pickle as pkl

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

        self._total_scores = []
        self._total_score_emas = []
        self._todays_macros = {}
        self._pomodoro_dic = {}

        self._seconds_of_day = 0
        self._date_int = 0
        self.last_score_update_timestamp = 0

        # init timed message was set
        self._timed_message_read = [False for _ in self._config.timed_messages()]

        # init dataframes
        self.update_time(is_init=True)
        self._read_dataframes()

        # init checkbox variables
        self._checkbox_variable_dic = {}
        for habit in self._config.habits():
            self._checkbox_variable_dic[habit.name()] = IntVar()
        for habit in self._config.sequence_habits():
            self._checkbox_variable_dic[habit.name()] = IntVar()

        if self._checkbox_df is not None:
            for check_name in self._checkbox_variable_dic:
                self._checkbox_variable_dic[check_name].set(
                    self._checkbox_df[self._checkbox_df.name == check_name].value.values[0])

        # init progressbar variables
        self._progressbar_variables = [DoubleVar() for _ in PROGRESSBAR_NAME_DIC.keys()]

        # update scores
        self.update_scores()
        self.need_to_update_scores = False

    def update_time(self, is_init=False):
        date_int = self._helper.get_date_int()
        self._seconds_of_day = self._helper.get_seconds_of_day()
        if date_int != self._date_int and not is_init:
            self._scores['pomodoro_minutes'] = 0
            self._scores['exercise_minutes'] = 0
            self._timed_message_read = [False for _ in self._config.timed_messages()]
            self._dump_dataframes()
            self._date_int = date_int
            self._read_dataframes()
            self.update_scores()
        self._date_int = date_int

    def update_pomodoro_dic(self):
        data_path = self._config.data_path()
        file_path = os.sep.join([data_path, 'pomodoro_dic.pkl'])
        if os.path.isfile(file_path):
            infile = open(file_path, 'rb')
            self._pomodoro_dic = pkl.load(infile)
            infile.close()

    def _read_dataframes(self):
        print('reading dataframes...')
        data_path = self._config.data_path()

        # foods
        self.reload_foods_df()

        # today's food hist
        file_path = os.sep.join([data_path, 'food_hists', str(self._date_int) + '.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._food_hist_df = pd.read_csv(file_path)
        else:
            self._food_hist_df = None

        # today's checkbox hist
        file_path = os.sep.join([data_path, 'checkbox_hists', str(self._date_int) + '.csv'])
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
        self._load_todays_minutes_from_scores()

    def _load_todays_minutes_from_scores(self):
        print('loading todays minutes from scores...')
        if self._scores_hist_df is not None:
            if self._date_int in self._scores_hist_df['date'].values:
                scores_hist_df_ = self._scores_hist_df[self._scores_hist_df['date'] == self._date_int]
                assert len(scores_hist_df_) == 1
                self._scores['pomodoro_minutes'] = scores_hist_df_['pomodoro_minutes'].values[0]
                self._scores['exercise_minutes'] = scores_hist_df_['exercise_minutes'].values[0]

    def reload_foods_df(self):
        print('reloading foods df...')
        while True:
            try:
                data_path = self._config.data_path()
                file_path = os.sep.join([data_path, 'foods.csv'])
                self._foods_df = pd.read_csv(file_path)
                self._foods_df['name'] = self._foods_df['name'].apply(lambda x: x.replace(' ', '_'))
                break
            except ValueError:
                print('WARNING - COULD NOT OPEN Foods.csv! retrying...')
                time.sleep(1)

        # add calories columns
        self._foods_df['fat_kcal'] = self._foods_df['fat_g'] * CALORIES_PER_GRAM_FAT
        self._foods_df['protein_kcal'] = self._foods_df['protein_g'] * CALORIES_PER_GRAM_PROTEIN
        self._foods_df['carb_kcal'] = self._foods_df['carb_g'] * CALORIES_PER_GRAM_CARB

    def _dump_dataframes(self):
        print('dumping dataframes...')
        self._dump_food_hist_df()
        self._dump_checkbox_df()
        self._dump_scores_hist_df()

    def _dump_food_hist_df(self):
        if self._food_hist_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'food_hists', str(self._date_int) + '.csv'])
            while True:
                try:
                    self._food_hist_df.to_csv(file_path, index=False)
                    break
                except PermissionError as e:
                    print(f'WARNING - {e}')
                    time.sleep(1)

    def _dump_checkbox_df(self):
        if self._checkbox_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'checkbox_hists', str(self._date_int) + '.csv'])
            while True:
                try:
                    self._checkbox_df.to_csv(file_path, index=False)
                    break
                except PermissionError as e:
                    print(f'WARNING - {e}')
                    time.sleep(1)

    def _dump_scores_hist_df(self):
        if self._scores_hist_df is not None:
            file_path = os.sep.join([self._config.data_path(), 'scores_hist.csv'])
            while True:
                try:
                    self._scores_hist_df.to_csv(file_path, index=False)
                    break
                except PermissionError as e:
                    print(f'WARNING - {e}')
                    time.sleep(1)

    def update_scores(self):
        print('s', end='')
        self.last_score_update_timestamp = time.time()

        # compute 'time score'

        if self.get_seconds_of_day() > self._config.get_up_seconds_of_day():
            time_passed = self.get_seconds_of_day() - self._config.get_up_seconds_of_day()
        else:
            time_passed = self.get_seconds_of_day() + (SECONDS_IN_DAY - self._config.get_up_seconds_of_day())
        self._scores['time'] = min(100, 100 * time_passed / (SECONDS_IN_DAY - self._config.sleep_duration_seconds()))

        # compute today's macros
        self._todays_macros = {}
        for macro in ['carb_kcal', 'fat_kcal', 'protein_kcal', 'water']:
            self._todays_macros[macro] = 0
        if self._food_hist_df is not None:
            for food_hist_row in self._food_hist_df.to_dict(orient="records"):
                food_name = food_hist_row['name']
                food_q = food_hist_row['qty']
                for macro in self._todays_macros:
                    self._todays_macros[macro] += float(food_q) * float(
                        self._foods_df[self._foods_df['name'] == food_name][macro].values[0])
        self._todays_macros['kcal'] = (self._todays_macros['carb_kcal']
                                       + self._todays_macros['fat_kcal']
                                       + self._todays_macros['protein_kcal'])

        # penalize if going over [0,100]
        self._scores['kcal'] = max(0, 1 - abs(self._todays_macros['kcal'] / self._config.kcal_target() - 1)) * 100
        # flat at max [0,100]
        self._scores['water'] = min(1, self._todays_macros['water'] / self._config.water_target()) * 100
        # flat at max [0,100]
        self._scores['protein'] = min(1, self._todays_macros['protein_kcal'] / self._config.protein_target()) * 100
        # start dropping over max [0,100]
        self._scores['carb'] = max(0,
                                   (1 - abs(self._todays_macros['carb_kcal'] / self._config.carb_target() - 1))) * 100
        # flat at max [0,100]
        self._scores['fat'] = min(1, self._todays_macros['fat_kcal'] / self._config.fat_target()) * 100

        # weighted linear combination of sub scores [0,100]
        self._scores['main_macros'] = (self._scores['kcal'] * 2.
                                       + self._scores['water'] * 3.
                                       + self._scores['protein']
                                       + self._scores['carb']
                                       + self._scores['fat']) / 8 * 1.2

        pomodoro_dic_minutes = 0
        if self._date_int in self._pomodoro_dic:
            pomodoro_dic_minutes = self._pomodoro_dic[self._date_int]
        self._scores['main_work'] = min(1.5, (self._scores['pomodoro_minutes'] + pomodoro_dic_minutes)
                                        / self._config.pomodoro_minutes_target()) * 100
        self._scores['main_sports'] = min(1.2, self._scores['exercise_minutes']
                                          / self._config.exercise_minutes_target()) * 100

        # compute habit score
        self._scores['main_habits'] = 0
        if self._checkbox_df is not None:
            temp = 0
            for habit in self._config.habits() + self._config.sequence_habits():
                checkbox_state = self._checkbox_df[self._checkbox_df['name'] == habit.name()]['value'].values[0]
                self._scores['main_habits'] += checkbox_state * habit.weight()
                temp += habit.weight()
            self._scores['main_habits'] /= temp / 100

        self._scores['total'] = (self._scores['main_work'] * 1 +
                                 self._scores['main_sports'] * 0.5 +
                                 self._scores['main_macros'] * 0.5 +
                                 self._scores['main_habits'] * 1) / 3

        # update and dump score hist df
        self._scores['date'] = self._date_int
        df_new = pd.DataFrame(self._scores, index=[0])
        if self._scores_hist_df is None:
            self._scores_hist_df = df_new
        else:
            self._scores_hist_df = self._scores_hist_df[self._scores_hist_df['date'] != self._date_int]
            self._scores_hist_df = pd.concat([self._scores_hist_df, df_new], axis=0, ignore_index=True)

        # compute score hist time series
        self._total_scores = self._scores_hist_df['total'].values
        half_life_factor = self._config.score_half_life_factor()
        self._total_score_emas = []
        score_ema_n = 0
        score_ema_d = 1. / (1. - half_life_factor)
        for total_score in self._total_scores:
            score_ema_n = score_ema_n * half_life_factor + total_score
            score_ema_d = score_ema_d * half_life_factor + 1
            self._total_score_emas.append(score_ema_n / score_ema_d)

        self._dump_scores_hist_df()

    def add_to_food_hist(self, timestamp, food_name, food_qty):
        df_new = pd.DataFrame([[timestamp, food_name, food_qty]], columns=['timestamp', 'name', 'qty'])
        if self._food_hist_df is None:
            self._food_hist_df = df_new
        else:
            self._food_hist_df = pd.concat([self._food_hist_df, df_new], axis=0, ignore_index=True)
        self._dump_food_hist_df()

    def remove_from_food_hist(self, index):
        self._food_hist_df.drop(index, inplace=True)
        self._food_hist_df.reset_index(inplace=True, drop=True)
        self._dump_food_hist_df()

    def update_checkbox_df(self):
        check_names = []
        check_values = []
        for check in self._checkbox_variable_dic:
            val = self._checkbox_variable_dic[check].get()
            check_names.append(check)
            check_values.append(val)
        self._checkbox_df = pd.DataFrame({'name': check_names, 'value': check_values})
        self._dump_checkbox_df()
        self.need_to_update_scores = True

    def get_checkbox_df(self):
        return self._checkbox_df

    def get_checkbox_variable_dic(self):
        return self._checkbox_variable_dic

    def get_seconds_of_day(self):
        return self._seconds_of_day

    def get_scores(self):
        return self._scores

    def get_date_int(self):
        return self._date_int

    def get_progressbar_variables(self):
        return self._progressbar_variables

    def get_timed_message_read(self):
        return self._timed_message_read

    def get_food_names(self):
        return list(self._foods_df['name'].values)

    def get_foods_df(self):
        return self._foods_df

    def get_food_hist_df(self):
        return self._food_hist_df

    def get_pomodoro_dic(self):
        return self._pomodoro_dic

    def get_total_score_emas(self):
        return self._total_score_emas

    def get_total_scores(self):
        return self._total_scores

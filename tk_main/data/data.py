import pandas as pd
import os

from ..helpers import *
from ..config import DATA_PATH, MACRO_TARGET_CONFIG, EXERCISE_MINUTES_TARGET
from ..config import POMODORO_MINUTES_TARGET, HABIT_CHECKLIST


class Data:

    def __init__(self):
        self._foods_df = None
        self._food_hist_df = None
        self._checkbox_df = None
        self._scores_hist_df = None

        self._macro_targets = {}
        self._scores = {'pomodoro_minutes': 0.,
                        'exercise_minutes': 0.}
        self._todays_macros = {}

        self._date_str = ''
        self._do_update_stats = False
        self._do_update_scores_hist = True

        print('initializing data...')
        self._init_macro_targets()
        self._update_time(is_init=True)
        self._read_dataframes()
        self._update_scores()

    def _init_macro_targets(self):
        assert (MACRO_TARGET_CONFIG['carb_ratio']
                + MACRO_TARGET_CONFIG['fat_ratio'] + MACRO_TARGET_CONFIG['protein_ratio']) == 1
        self._macro_targets['kcal'] = MACRO_TARGET_CONFIG['kcal_target']
        self._macro_targets['carb'] = MACRO_TARGET_CONFIG['kcal_target'] * MACRO_TARGET_CONFIG['carb_ratio']
        self._macro_targets['fat'] = MACRO_TARGET_CONFIG['kcal_target'] * MACRO_TARGET_CONFIG['fat_ratio']
        self._macro_targets['protein'] = MACRO_TARGET_CONFIG['kcal_target'] * MACRO_TARGET_CONFIG['protein_ratio']
        self._macro_targets['water'] = MACRO_TARGET_CONFIG['water_target']

    def _update_time(self, is_init=False):
        date_str = get_date_str()
        if date_str != self._date_str and not is_init:
            self._process_date_change()
        self._date_str = date_str

    def _process_date_change(self):
        # this function is still running on the old date string
        print('processing date change!')
        self._dump_dataframes()
        self._read_dataframes()
        self._update_scores()

    def _read_dataframes(self):
        # foods
        file_path = os.sep.join([DATA_PATH, 'Foods.csv'])
        self._foods_df = pd.read_csv(file_path)
        self._foods_df['food'] = self._foods_df['food'].apply(lambda x: x.replace(' ', '_'))

        # today's food hist
        file_path = os.sep.join([DATA_PATH, 'food_hists', self._date_str + '.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._food_hist_df = pd.read_csv(file_path)
        else:
            self._food_hist_df = None

        # today's checkbox hist
        file_path = os.sep.join([DATA_PATH, 'checkbox_hists', self._date_str + '.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._checkbox_df = pd.read_csv(file_path)
        else:
            self._checkbox_df = None

        # score hist
        file_path = os.sep.join([DATA_PATH, 'scores_hist.csv'])
        if os.path.isfile(file_path):
            with open(file_path):
                self._scores_hist_df = pd.read_csv(file_path)
        else:
            self._scores_hist_df = None

    def _dump_dataframes(self):
        self._foods_df()
        self._dump_food_hist_df()
        self._dump_checkbox_df()
        self._dump_scores_hist_df()

    def _dump_foods_df(self):
        if self._foods_df is not None:
            file_path = os.sep.join([DATA_PATH, 'Foods.csv'])
            self._foods_df.to_csv(file_path)

    def _dump_food_hist_df(self):
        if self._food_hist_df is not None:
            file_path = os.sep.join([DATA_PATH, 'food_hists', self._date_str + '.csv'])
            self._food_hist_df.to_csv(file_path)

    def _dump_checkbox_df(self):
        if self._checkbox_df is not None:
            file_path = os.sep.join([DATA_PATH, 'checkbox_hists', self._date_str + '.csv'])
            self._checkbox_df.to_csv(file_path)

    def _dump_scores_hist_df(self):
        if self._scores_hist_df is not None:
            file_path = os.sep.join([DATA_PATH, 'scores_hist.csv'])
            self._scores_hist_df.to_csv(file_path)

    def add_to_food_hist(self, timestamp, food_name, food_qty):
        self._update_time()
        df_new = pd.DataFrame([[timestamp, food_name, food_qty]], columns=['timestamp', 'food', 'qty'])
        if self._food_hist_df is None:
            self._food_hist_df = df_new
        else:
            self._food_hist_df = pd.concat([self._food_hist_df, df_new], axis=0, ignore_index=True)
        self._dump_food_hist_df()
        self._update_scores()

    def remove_from_food_hist(self, index):
        self._food_hist_df.drop(index, inplace=True)
        self._food_hist_df.reset_index(inplace=True, drop=True)
        self._dump_food_hist_df()
        self._update_scores()

    def update_checkbox_df(self, check_dictionary):
        check_names = []
        check_values = []
        for check in check_dictionary:
            val = check_dictionary[check].get()
            check_names.append(check)
            check_values.append(val)
        self._checkbox_df = pd.DataFrame({'name': check_names, 'value': check_values})
        self._dump_checkbox_df()
        self._update_scores()

    def _update_scores(self):

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
        self._scores['kcal'] = max(0, 1 - abs(self._todays_macros['kcal'] / self._macro_targets['kcal'] - 1)) * 100
        # flat at max [0,100]
        self._scores['water'] = min(1, self._todays_macros['water'] / self._macro_targets['water']) * 100
        # flat at max [0,100]
        self._scores['protein'] = min(1, self._todays_macros['protein'] / self._macro_targets['protein']) * 100
        # start dropping over max [0,100]
        self._scores['carb'] = max(0, 1 - max(0, self._todays_macros['carb'] / self._macro_targets['carb'] - 1)) * 100
        # flat at max [0,100]
        self._scores['fat'] = min(1, self._todays_macros['fat'] / self._macro_targets['fat']) * 100

        # weighted linear combination of sub scores [0,100]
        self._scores['main_macros'] = (self._scores['kcal'] * 2.
                                       + self._scores['water'] * 3.
                                       + self._scores['protein']
                                       + self._scores['carb']
                                       + self._scores['fat']) / 8 * 1.2

        self._scores['main_work'] = min(1.5, self._scores['pomodoro_minutes'] / POMODORO_MINUTES_TARGET) * 100
        self._scores['main_sports'] = min(1.2, self._scores['exercise_minutes'] / EXERCISE_MINUTES_TARGET) * 100

        # compute habit score
        self._scores['main_habits'] = 0
        if self._checkbox_df is not None:
            temp = 0
            for habit in HABIT_CHECKLIST:
                checkbox_state = self._checkbox_df[self._checkbox_df['name'] == habit[0]]['value'].values[0]
                self._scores['main_habits'] += checkbox_state * habit[1]
                temp += habit[1]
            self._scores['main_habits'] /= temp / 100

        self._scores['total'] = (self._scores['main_work'] * 1 +
                                 self._scores['main_sports'] * 1 +
                                 self._scores['main_macros'] * 1 +
                                 self._scores['main_habits'] * 1) / 4

        print(self._scores)
        self.do_update_stats = True

        # update and dump score hist df
        date = get_date_str()
        self._scores['date'] = date
        df_new = pd.DataFrame(self._scores, index=[0])

        if self._scores_hist_df is None:
            self._scores_hist_df = df_new
        else:
            self._scores_hist_df = self._scores_hist_df[self._scores_hist_df['date'] != date]
            self._scores_hist_df = pd.concat([self._scores_hist_df, df_new], axis=0, ignore_index=True)

        self._dump_scores_hist_df()
        self._do_update_scores_hist = True

    def get_checkbox_df(self):
        return self._checkbox_df

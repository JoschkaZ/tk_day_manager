from typing import List
import numpy as np

from ._static import *


class Habit:
    def __init__(self, name, weight):
        self._NAME = name
        self._WEIGHT = weight

    def name(self):
        return self._NAME

    def weight(self):
        return self._WEIGHT


class TimedMessage:
    def __init__(self, text, seconds_of_day):
        self._TEXT = text
        self._SECONDS_OF_DAY = seconds_of_day

    def text(self):
        return self._TEXT

    def seconds_of_day(self):
        return self._SECONDS_OF_DAY


class Config:
    def __init__(self, yaml_dic):
        self._DATA_PATH = yaml_dic['DATA_PATH']

        self._TIMEZONE_STR = yaml_dic['TIMEZONE_STR']

        self._KCAL_TARGET = yaml_dic['KCAL_TARGET']
        self._WATER_TARGET = yaml_dic['WATER_TARGET']
        self._compute_macro_targets(yaml_dic)

        self._EXERCISE_MINUTES_TARGET = yaml_dic['EXERCISE_MINUTES_TARGET']

        self._POMODORO_MINUTES_TARGET = yaml_dic['POMODORO_MINUTES_TARGET']

        self._GET_UP_SECONDS_OF_DAY = yaml_dic['GET_UP_HOUR'] * SECONDS_IN_HOUR
        self._SLEEP_DURATION_SECONDS = yaml_dic['SLEEP_DURATION_HOURS'] * SECONDS_IN_HOUR
        self._GO_TO_BED_SECONDS_OF_DAY = (
                self._GET_UP_SECONDS_OF_DAY + SECONDS_IN_DAY - self._SLEEP_DURATION_SECONDS) % SECONDS_IN_DAY

        self._HABITS: List[Habit] = []
        self._SEQUENCE_HABITS: List[Habit] = []
        self._parse_habits(yaml_dic)

        self._TIMED_MESSAGES: List[TimedMessage] = []
        self._N_WAKE_DAY_SECTION_MESSAGES = yaml_dic['N_WAKE_DAY_SECTION_MESSAGES']
        self._parse_timed_messages(yaml_dic)

        self._POMODORO_TIMER_MINUTE_OPTIONS = yaml_dic['POMODORO_TIMER_MINUTE_OPTIONS']

        self._SCORE_HALF_LIFE = yaml_dic['SCORE_HALF_LIFE']
        self._SCORE_HALF_LIFE_FACTOR = 0.5**(1 / self._SCORE_HALF_LIFE)

    def _compute_macro_targets(self, yaml_dic):
        assert yaml_dic['CARB_RATIO'] + yaml_dic['FAT_RATIO'] + yaml_dic['PROTEIN_RATIO'] == 1
        self._CARB_TARGET = self._KCAL_TARGET * yaml_dic['CARB_RATIO']
        self._FAT_TARGET = self._KCAL_TARGET * yaml_dic['FAT_RATIO']
        self._PROTEIN_TARGET = self._KCAL_TARGET * yaml_dic['PROTEIN_RATIO']

    def _parse_habits(self, yaml_dic):
        for habit_name in yaml_dic['HABITS']:
            habit_weight = yaml_dic['HABITS'][habit_name]
            self._HABITS.append(Habit(habit_name, habit_weight))

        for habit_name in yaml_dic['SEQUENCE_HABITS']:
            habit_weight = yaml_dic['SEQUENCE_HABITS'][habit_name]
            self._SEQUENCE_HABITS.append(Habit(habit_name, habit_weight))

    def _parse_timed_messages(self, yaml_dic):
        texts = []
        seconds_of_days = []
        for text in yaml_dic['TIMED_MESSAGES']:
            hour_delta = yaml_dic['TIMED_MESSAGES'][text]

            if hour_delta >= 0:
                seconds_of_day = int(self._GET_UP_SECONDS_OF_DAY + hour_delta * SECONDS_IN_HOUR)
            else:
                seconds_of_day = int(self._GO_TO_BED_SECONDS_OF_DAY + hour_delta * SECONDS_IN_HOUR)
            texts.append(text)
            seconds_of_day = seconds_of_day % SECONDS_IN_DAY
            seconds_of_days.append(seconds_of_day)

        print('message seconds: ', seconds_of_days)

        if self._GO_TO_BED_SECONDS_OF_DAY < self._GET_UP_SECONDS_OF_DAY:
            section_seconds_of_days = np.linspace(self._GET_UP_SECONDS_OF_DAY,
                                                  self._GO_TO_BED_SECONDS_OF_DAY + SECONDS_IN_DAY,
                                                  self._N_WAKE_DAY_SECTION_MESSAGES+1)
            section_seconds_of_days = [x % SECONDS_IN_DAY for x in section_seconds_of_days]
        else:
            section_seconds_of_days = np.linspace(self._GET_UP_SECONDS_OF_DAY, self._GO_TO_BED_SECONDS_OF_DAY,
                                                  self._N_WAKE_DAY_SECTION_MESSAGES+1)

        print('section: ', section_seconds_of_days)

        for i, section_seconds_of_day in enumerate(section_seconds_of_days):
            text = f"{np.round(i / self._N_WAKE_DAY_SECTION_MESSAGES * 100)} percent of the day is over."
            texts.append(text)
            seconds_of_days.append(int(section_seconds_of_day))

        # sort it
        texts = [y for x, y in list(sorted(zip(seconds_of_days, texts)))]
        seconds_of_days = list(sorted(seconds_of_days))

        # create timed messages
        for i in range(len(texts)):
            self._TIMED_MESSAGES.append(TimedMessage(texts[i], seconds_of_days[i]))

        for tm in self._TIMED_MESSAGES:
            print(tm.seconds_of_day(), tm.text())

    def data_path(self):
        return self._DATA_PATH

    def timezone_str(self):
        return self._TIMEZONE_STR

    def kcal_target(self):
        return self._KCAL_TARGET

    def water_target(self):
        return self._WATER_TARGET

    def carb_target(self):
        return self._CARB_TARGET

    def fat_target(self):
        return self._FAT_TARGET

    def protein_target(self):
        return self._PROTEIN_TARGET

    def exercise_minutes_target(self):
        return self._EXERCISE_MINUTES_TARGET

    def pomodoro_minutes_target(self):
        return self._POMODORO_MINUTES_TARGET

    def get_up_seconds_of_day(self):
        return self._GET_UP_SECONDS_OF_DAY

    def sleep_duration_seconds(self):
        return self._SLEEP_DURATION_SECONDS

    def go_to_bed_seconds_of_day(self):
        return self._GO_TO_BED_SECONDS_OF_DAY

    def habits(self):
        return self._HABITS

    def sequence_habits(self):
        return self._SEQUENCE_HABITS

    def timed_messages(self):
        return self._TIMED_MESSAGES

    def pomodoro_timer_minute_options(self):
        return self._POMODORO_TIMER_MINUTE_OPTIONS

    def score_half_life_factor(self):
        return self._SCORE_HALF_LIFE_FACTOR

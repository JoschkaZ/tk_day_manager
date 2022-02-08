
DATA_PATH = r'C:\coding\data\tk_day_manager'
SECONDS_IN_HOUR = 3600
SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR
TIMEZONE_STR = 'Europe/Berlin'

# food
MACRO_TARGET_CONFIG = {
  'kcal_target': 2500,
  'carb_ratio': .4,
  'fat_ratio': .3,
  'protein_ratio': .3,
  'water_target': 3000,
}

# exercise
EXERCISE_MINUTES_TARGET = 45

# work
POMODORO_MINUTES_TARGET = 360

# sleep
WAKE_SECONDS = 6.0 * SECONDS_IN_DAY
SLEEP_DURATION_SECONDS = 7 * SECONDS_IN_HOUR

_wake_duration_seconds = SECONDS_IN_DAY - SLEEP_DURATION_SECONDS
_bed_time = (WAKE_SECONDS + _wake_duration_seconds) % SECONDS_IN_DAY

# habits
HABIT_CHECKLIST = [
    ['Woke up early', 2],
    ['Glass of Water', 1],
    ['Morning Exercise', 1],
    ['Breakfast', 1],
    ['Protein Shake', 1],
    ['No Soft Drinks', 1],
    ['Flat is clean', 1],
    ['30 min Reading', 1],
]

# audio messages
TIMED_MESSAGES = [
    (WAKE_SECONDS + 0.5 * SECONDS_IN_HOUR, 'good morning.'),
    (_bed_time - 6.5 * SECONDS_IN_HOUR, 'drink last coffee now.'),
    (_bed_time - 6.0 * SECONDS_IN_HOUR, 'no more coffee for today.'),
    (_bed_time - 4.0 * SECONDS_IN_HOUR, 'eat last food now.'),
    (_bed_time - 3.0 * SECONDS_IN_HOUR, 'no more food for today.'),
    (_bed_time - 3.0 * SECONDS_IN_HOUR, 'three hours left.'),
    (_bed_time - 2.0 * SECONDS_IN_HOUR, 'two hours left.'),
    (_bed_time - 1.0 * SECONDS_IN_HOUR, 'one hour left.'),
    (_bed_time - 0.5 * SECONDS_IN_HOUR, 'prepare to sleep in thirty minutes.'),
    (_bed_time, 'you should be sleeping now.')
]

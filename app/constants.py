import logging

LONG_LINE = '-' * 50

MENU_CHOOSE_KEY = """
Interactive Manager
Please choose what task do you want to manage.

1. Tasks
2. Users
3. Exit

Number [3]: """

MENU_CHOOSE_ACTION = """
Interactive Manager
Please choose action for key `%s`:

1. Add
2. Remove
3. Show
4. Exit

Number [4]: """

SHOW_USER_PLANS = """
User: %s
        [
            efficiency: %.2f%%,
            tasks: %r
            all_points: %d
            remain_points: %d
        ]
"""

SHOW_CONCLUSION = """
Conclusion:
    The min of remain task points left: %d
    The max of user points left: %d
    Remain tasks: %r
    Complex tasks: %r
    Assigned tasks: %r
"""

LOGGING_CONFIGURATIONS = dict(
    format='%(asctime)s -> %(levelname)s :  %(message)s',
    level=logging.DEBUG
)

INPUT_FILENAME = 'sb_info.json'
LOG_FILENAME = 'sb_log.log'
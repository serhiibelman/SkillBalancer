import json
import logging

import app.constants as consts

logger = logging.getLogger()


class InteractiveMode:
    """
    This class provides an ability to manipulate a json data over the
    interactive menu. This helps to more understandable manage json,
    including adding/removing/showing a data.
    """

    def __init__(self):

        with open(consts.INPUT_FILENAME) as fp:
            self.data = get_json_from_file(fp)
        self.key = None
        self.id_item = ''

    def interactive_manager_menu(self):
        """
        Running the simple console interactive manager.

        ----------------------------------------------
        Interactive Manager
        Please choose what task do you want to manage.

        1. Tasks
        2. Users
        3. Exit

        Number [3]:
        ----------------------------------------------

        :return: None
        """
        logger.info("Starting interactive manager.")
        print(consts.LONG_LINE)
        
        while True:
            
            option = input(consts.MENU_CHOOSE_KEY)
            print(consts.LONG_LINE)
            if option == '1':
                self.key = 'tasks'
            elif option == '2':
                self.key = 'users'
            else:
                # this means a user don't need interactive mode enymore
                return False
            # go over to Interactive action menu
            self.run_action_manager()

    def run_action_manager(self):

        with open(consts.INPUT_FILENAME) as fp:
            # check correctness of json file, will quit if don't fit.
            check_json_health(fp) # fail need to rewrite
            # running the menu of actions (add/remove/show)
            self.menu_action_loop()
        # Save JSON file with changes
        save_data_to_file(self.data)

    def menu_action_loop(self):

        """
        Running action menu

        ------------------------------------
        Interactive Manager
        Please choose action for key `%s`:

        1. Add      +
        2. Remove   +-
        3. Show     +-
        4. Exit     +

        Number [4]:
        ------------------------------------ 
        """

        while True:
        
            option = input(consts.MENU_CHOOSE_ACTION % self.key)

            if option == '2' or option == '3':
                self.item_id = input(
                    'Provide the item ID(username or task name): '
                    )
            # printing horizontal line for better perception of viewer.
            print(consts.LONG_LINE + '\n')
            if option == '1':
                self.create_new_item()
            elif option == '2':
                self.remove_item()
            elif option == '3':
                print(self.data[self.key][self.item_id])
            else:
                break

        print('\n' + consts.LONG_LINE)

    def create_new_item(self):
        """
        This function creates and add new item to json data by given key.
        If nickname or points won't provide, will return and print to logs

        dict type value:
            name -> str
            points -> int
            tasks -> list
            efficiency -> int

        :return: None
        """
        # Should be a unique `name` in keys or will overwrite exist `name`.
        name = input("Name of item: ")
        # points should be a digit
        points = input("His points: ")
        if not (name and points):
            print_both_outputs(
                "You don't provide a nickname or points",
                logging.WARNING
                )
            return
        elif not (points.isdigit() and int(points) > 0):
            print_both_outputs(
                "Points should be digit and more than 0",
                logging.WARNING
                )
            return

        # creates a unique name with given key in dict.
        self.data[self.key].setdefault(name, {})
        # First we create count of points, because they neede to both keys.
        # So from here, task options are fully created.
        self.data[self.key][name] = {
            'points': int(points)
        }
        if self.key == 'users':
            # if key is `users`, we need to add two fields: efficiency of user
            # and tasks which he needs to do.
            self.data[self.key][name].update({
                'tasks': {},
                'efficiency': 0
            })
        print_both_outputs(
            "Item `%s` in key `%s` was successfully created" % (name, self.key),
            logging.DEBUG
        )

    def remove_item(self):
        """
        Removes an unique name of task or user, if it exists
        in `self.data[self.key]`. Applying action will show into logs.
        """
        if not self.item_id:
            print_both_outputs(
                "You don't provide a name to delete.",
                logging.WARNING
            )
            return
        # check if `self.item_id` exists in a data
        if self.item_id in self.data[self.key]:
            del self.data[self.key][self.item_id]
            print_both_outputs(
                "Item `%s` in key `%s` was successfully deleted" % (self.key, self.item_id),
                logging.DEBUG
            )
        else:
            print_both_outputs(
                "Item `%s` doesn't exist in key `%s`" % (self.item_id, self.key),
                logging.WARNING
            )

    def run(self):
        try:
            self.interactive_manager_menu()
        except json.decoder.JSONDecodeError:
            print_both_outputs(
                "Input file doesn't have JSON or JSON is broken. Quiting",
                logging.ERROR
            )
            exit(1)

class ConsoleColor:
    """
    This class provides more pretty color view for console. It can be used as:

    >>> with ConsoleColor(level=logging.DEBUG):
    >>>     print('Some your message with debug color')
    """

    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, level=None):
        """
        Initialize the class ConsoleColor and choose the particular color
        for giving level
        :param level: module `logging` levels or None
        """
        if level == logging.DEBUG:
            self.color = self.OK_GREEN
        elif level == logging.INFO:
            self.color = self.OK_BLUE
        elif level == logging.ERROR:
            self.color = self.FAIL
        elif level == logging.WARNING:
            self.color = self.WARNING
        else:
            self.color = self.WHITE

    def __enter__(self):
        """
        This function prints a color which was set in `__init__`

        :return: None
        """
        print(self.color)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        This function close a color which was set in `__init__` to white.

        :param exc_type: type of exc
        :param exc_val: value of exc
        :param exc_tb: traceback of exc

        :return: None
        """
        print(self.WHITE)

def print_both_outputs(msg, level=logging.DEBUG):
    """
    The function print info message on both sides (stdout and to output
    logs) with console colors.

    :param msg: str -> message which will be printed
    :param level: logging level name
    :return: None

    :notes: This function created only for interactive viewer.
    """
    with ConsoleColor(level):
        print(msg)
    logger.log(level, msg)

def get_json_from_file(fp):
    """
    Check json data in file for correctness structure, if keys don't fit
    standard, function will print info to log and quit application.

    :param fp: file descriptor
    :return: dict -> loaded json data from file
    """
    # reading the file and transform into JSON data.
    data = check_json_health(fp)
    if data is None:
        # if data is None, then something with keys wrong,
        # probably one of keys doesn't exist in data or both of them.
        # So we need to raise exception here.
        print_both_outputs(
            "JSON file doesn't have a key `tasks` or `users`. ",
            logging.ERROR
        )
        exit(1)
    logger.debug('JSON was successfully loaded from %s', consts.INPUT_FILENAME)
    return data

def check_json_health(fd):
    """
    Load a json from file and check existence of keys (`tasks` and `users`)
    in JSON data.

    :param fd: IO class, file descriptor
    :return: returns dict from loaded json data, or None if keys don't exist.
    """
    data = json.load(fd)
    if 'tasks' not in data or 'users' not in data:
        return None
    return data

def save_data_to_file(data, file=consts.INPUT_FILENAME):
    """
    Transform a dict into pretty json and save him to file.

    :return: None
    """
    with open(file, 'w') as fp:
        # save edited data into file `INPUT_FILENAME`
        json.dump(data, fp, indent=4)
        print_both_outputs('New changes have been saved successfully.')
import os
import json
import logging

import app.constants as consts

from app.algorithm import SkillBalancer
from app.command_parser import get_parsed_args
from app.interactive import InteractiveMode, logger, print_both_outputs


def set_logging(filename=None):
    """
    Setting the logging configuration by `logging` module. After, you can
    use `logger` to write log info.
    If filename is provided it will open it and write to file log info.

    :param filename: str - the name of file for output
    :return: None
    """
    logging.basicConfig(filename=filename, **consts.LOGGING_CONFIGURATIONS)

    if filename is None:
        logger.info("Output is set to stdout.")
    else:
        logger.info("Output is set to `%s`.", filename)

def check_input_file():
    """
    If file exists, function will skip.
    Otherwise, creates empty file with `INPUT_FILENAME` value and add
    empty json data.

    :return: None
    """
    if os.path.exists('sb_info.json'):
        logger.debug('Input file `%s` exists.', consts.INPUT_FILENAME)
        return False

    # will create file if it doesn't exist.
    with open(consts.INPUT_FILENAME, 'w') as fp:
        # adds to file empty tasks and users data with pretty intend in file
        json.dump(
            {'tasks': {}, 'users': {}}, fp, indent=True
        )
    logger.debug('Input file `%s` created.', consts.INPUT_FILENAME)
    return True

def main():

    # parsing args from command line, will get flags and args.
    parsed_args = get_parsed_args()

    set_logging(filename=parsed_args.output_file)
    # check input file, if it doesn't exist will create.

    check_input_file()
    if parsed_args.interactive_mode:
        InteractiveMode().run()
    
    if not parsed_args.avoid_sb:
        team = SkillBalancer()
        team.main_algorithm(show_plan=parsed_args.details, save_to_file=True)

    print_both_outputs("All done. Exiting.", logging.INFO)

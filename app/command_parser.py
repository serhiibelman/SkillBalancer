import argparse

from app.constants import LOG_FILENAME

def get_parsed_args():
    """
    Gives parsed arguments from command line.

    :returns: argparse.Namespace with parsed arguments
    """
    parser = argparse.ArgumentParser(
            prog="SkillBalancer",

            usage="Proper distribution of tasks among users",

            description="Skill Balancer (SB) is a console application for searching the"
                        "right decision to choose and distribute tasks among users.")

    # ==================================
    # Arguments for parsing command line
    # ==================================

    parser.add_argument('-i', '--interactive_mode',
                        nargs='?',
                        type=bool,
                        metavar='',
                        const=True,
                        default=False,
                        help='This parameter starts the interactive mode'
                        )

    parser.add_argument('-a', '--avoid_sb',
                        nargs='?',
                        type=bool,
                        metavar='',
                        const=True,
                        default=False,
                        help="When use, Skill Balancer will not plan a task "
                             "for users. For default, it's in use."
                        )

    parser.add_argument('-o', '--output_log',
                        nargs='?',
                        type=str,
                        metavar='',
                        const=True,
                        default=LOG_FILENAME,
                        help='This need if you want to change name of out log file',
                        dest='output_file'
                        )

    parser.add_argument('-n', '--hide-details',
                        nargs='?',
                        type=bool,
                        metavar='',
                        const=False,
                        default=True,
                        help="This option tells SB to show detailed "
                             "information about what TeamBalancer did.",
                        dest='details'
                        )

    return parser.parse_args()
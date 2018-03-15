import argparse
import os
import unittest

from app.interactive import logger
from app.balancer import set_logging, check_input_file
from app.constants import LOG_FILENAME, INPUT_FILENAME


class TestMainFile(unittest.TestCase):
    def setUp(self):
        # base folder of project
        self.abs_dir_path = os.path.dirname(os.path.abspath(__name__))

    def test_set_logging(self):
        """
        Testing the correct configs of logging file, if it was given.
        """
        set_logging(LOG_FILENAME)
        # check for created file
        self.assertTrue(
            os.path.exists(os.path.join(
                self.abs_dir_path, LOG_FILENAME)
            )
        )
        # check logging into `LOG_FILENAME`
        logger.debug('test_set_logging message')
        with open(LOG_FILENAME) as fp:
            self.assertTrue(
                fp.readlines()[-1],
                '2018-03-01 18:21:51,760 -> DEBUG :  test_set_logging message'
            )

    @unittest.skip
    def test_check_input_file(self):
        """
        Testing the `check_input_file` for correctness creation of input file
        """
        # test the creation of `LOG_FILENAME` if it doesn't exist
        print(os.path.join(self.abs_dir_path, LOG_FILENAME))
        os.remove(os.path.join(self.abs_dir_path, LOG_FILENAME))
        # need to be created
        self.assertTrue(check_input_file())
        # already exists
        self.assertFalse(check_input_file())

    def test_get_parsed_args(self):
        """
        Testing the correctness of parsed arguments.
        """
        parser = get_parser()
        # without any args
        parsed_args = parser.parse_args([])
        self.assertFalse(parsed_args.interactive_mode)
        self.assertFalse(parsed_args.avoid_sb)
        self.assertEqual(parsed_args.output_file, LOG_FILENAME)
        self.assertTrue(parsed_args.details)

        # with args
        parser = get_parser()
        parsed_args = parser.parse_args(
            ['-i', '-n', '-o' 'my_file', '--avoid_sb']
        )
        self.assertTrue(parsed_args.interactive_mode)
        self.assertEqual(parsed_args.output_file, 'my_file')
        self.assertFalse(parsed_args.details)
        self.assertTrue(parsed_args.avoid_sb)


def get_parser():
    """
    modification copy of app.command_parser.get_parsed_args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--interactive_mode', metavar='', nargs='?', type=bool,
                        const=True, default=False)

    parser.add_argument('-a', '--avoid_sb', nargs='?', metavar='', type=bool, const=True,
                        default=False)

    parser.add_argument('-o', '--output_log', nargs='?', metavar='', type=str,
                        default=LOG_FILENAME, dest='output_file')

    parser.add_argument('-n', '--hide-details', nargs='?', metavar='', type=bool,
                        const=False, default=True, dest='details')

    return parser

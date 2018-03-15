import json
import sys
import unittest

import app.interactive as interactive


class TestInteractManagerTools(unittest.TestCase):
    def setUp(self):
        # test input file
        self.test_file_name = 'sb-testing-data.json'

    # def test_get_pretty_json(self):
    #     """
    #     Testing for correctness of creation pretty json to file
    #     """
    #     data = {
    #         'key1': {
    #             'key2': [1, 2]
    #         }
    #     }
    #     self.assertEqual(
    #         interactive.get_pretty_json(data, 'key1', 'key2'),
    #         json.dumps([1, 2], indent=4, sort_keys=True)
    #     )

    def test_check_json_health(self):
        """
        Testing the json for corruption.
        """
        # check health json
        with open(self.test_file_name, 'w') as fp:
            json.dump({'tasks': {}, 'users': {}}, fp)

        with open(self.test_file_name) as fp:
            self.assertEqual(
                interactive.check_json_health(fp),
                {'tasks': {}, 'users': {}}
            )

        # check corrupted json
        with open(self.test_file_name, 'w') as fp:
            json.dump({'tasks': {}}, fp)

        with open(self.test_file_name) as fp:
            self.assertIsNone(interactive.check_json_health(fp))

    def test_save_data_to_file(self):
        """
        Testing the correctness of transforming dict to json and after saving
        """
        data = {
            'fir': 5,
            'sec': [],
            'some more': {}
        }
        with open('sb-testing-output.txt', 'w') as fp:
            sys.stdout = fp
            interactive.save_data_to_file(data, self.test_file_name)

        with open(self.test_file_name) as fp:
            self.assertEqual(json.load(fp), data)

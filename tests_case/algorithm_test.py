import random
import time
import unittest

from app.algorithm import SkillBalancer


class TestSkillBalancer(unittest.TestCase):
    def setUp(self):
        self.sb = SkillBalancer()
        # generates random 10000 tasks and 2000 users
        self.sb.data = generate_random_data(10000, 2000)

    def test_get_name_and_points_by_key(self):
        """
        Testing the correctness of users and tasks creation.
        """
        users = list(self.sb.get_name_and_points_by_key('users'))
        tasks = list(self.sb.get_name_and_points_by_key('tasks'))

        # checks correct creation of users
        self.assertEqual(len(users), len(self.sb.data['users']))
        self.assertEqual(len(users[0]), 2)
        self.assertIsInstance(users[0], list)
        self.assertTrue(users[0])

        # checks correct creation of tasks
        self.assertEqual(len(tasks), len(self.sb.data['tasks']))
        self.assertEqual(len(tasks[0]), 2)
        self.assertIsInstance(users[0], list)
        self.assertTrue(tasks[0])

    def test_sort_data_by_point(self):
        """
        Check if function sorts properly.
        :return:
        """
        # empty users and tasks
        self.assertFalse(self.sb.users)
        self.assertFalse(self.sb.tasks)

        self.sb.sort_data_by_point()

        # fill out users and tasks
        self.assertTrue(self.sb.users)
        self.assertTrue(self.sb.tasks)

        # Check if sorted properly
        first_u = random.choice(self.sb.users)
        second_u = random.choice(self.sb.users)
        first_inx = self.sb.users.index(first_u)
        second_inx = self.sb.users.index(second_u)
        # As example if `first_inx` == 5 and `second_inx` == 2
        # then more bigger points should be in `second_inx` as it reversed
        if first_inx > second_inx:
            self.assertGreater(second_u[1], first_u[1])
        else:
            self.assertLessEqual(second_u[1], first_u[1])

    def test_refresh_user_tasks(self):
        """
        Testing function for cleaning old users tasks
        """
        self.sb.sort_data_by_point()
        self.sb.data['users']['user_500']['tasks'] = {
            "Some a great task": 50
        }

        self.sb.drop_users_tasks()
        self.assertFalse(self.sb.data['users']['user_500']['tasks'])

    def test_main_algorithm_speed(self):
        """
        Testing the schedule speed.
        :return:
        """
        now = time.time()
        self.sb.main_algorithm()
        print("Working time:", time.time() - now)
        print("Users number:", self.sb.users_number)
        print("Tasks number:", len(self.sb.tasks))
        

def generate_random_data(task_number=100, user_number=50):
    data = {}
    tasks = ('task_' + str(number) for number in range(task_number))
    users = ('user_' + str(number) for number in range(user_number))
    keys = (('tasks', tasks), ('users', users))
    for key, names in keys:
        data[key] = set_random_data(key, names)
    return data


def set_random_data(key, names):
    data = {}
    for name in names:
        data[name] = {'points': random.randint(25, 90)}
        if key == 'users':
            data[name].update({
                'tasks': {},
                'efficiency': 0
            })
        else:
            data[name] = {'points': random.randint(10, 100)}

    return data
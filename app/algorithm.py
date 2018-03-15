import app.constants as consts

from app.interactive import get_json_from_file, save_data_to_file
from app.interactive import logger, ConsoleColor, print_both_outputs

class SkillBalancer(object):
	"""
	Class provides a building scheduler algorithm. It helps to distribute
    the right tasks for every user, so no one will stay without work and
    users will take task that they could work with their level and complete.

    For more details about algorithm, see `main_algorithm` and `task_allocator` funcs.
	"""

	def __init__(self):

		with open(consts.INPUT_FILENAME) as fp:
			self.data = get_json_from_file(fp)

		self.tasks = []
		self.users = []

		self.complex_tasks = set()
		self.remain_tasks = set()
		self.applied_tasks = set()

		self.remain_points = dict()

		self.tasks_number = 0
		self.users_number = 0

		self.min_task_point = 0
		self.max_users_point = 0
		self.max_remain_user_point = 0

	def get_name_and_points_by_key(self, key):
		"""
        Function returns a list of names and points a key.
        Key can only be `tasks` or `users`. As interactive manager saves
        to input file:
        
        :param key: str -> can be `tasks` or `users`
        :return: generator -> [name, points]
        """

		for name in self.data[key]:
			yield [name, self.data[key][name]['points']]

	def sort_data_by_point(self):
		"""
        Function sorts a reversed data by points
        and saves it to keys (can only be `tasks` or `users`)

        :return: None
        """

		for key in ('tasks', 'users'):
			self.__dict__[key] = sorted(
				self.get_name_and_points_by_key(key),
				key=lambda x: x[1],
				reverse=True
				)

	def drop_users_tasks(self):
		"""
		Function clean all tasks which set in [users]
		and add `remain_points` to the data
		---------------------------
        {
            "tasks": {
                "First task": {
                    "points": 45
                }
            },
            "users": {
                "John": {
                    "points": 0,
                    "efficiency": 0,
                    "tasks": {},
                    "remain_points", 0
                }
            }
        }
        ---------------------------
		:return: None
		"""

		users = self.data['users']

		for name in users:
			users[name]['tasks'].clear()
			self.remain_points = {'remain_points': users[name]['points']}
			users[name].update(self.remain_points)
		logger.debug('Old user tasks was successfully dropped.')

	def _set_tasks_number(self):
		"""
		Count number of tasks and set to `task_number`

		:return: None
		"""
		self.tasks_number = len(self.tasks)

	def _set_users_number(self):
		"""
		Count number of users and set to `users_number`

		:return: None
		"""
		self.users_number = len(self.users)
		logger.debug('Users number: %d', self.users_number)

	def _set_min_task_point(self):
		"""
		Set minimum task point

		:return: None
		"""
		if self.tasks:
			self.min_task_point = self.tasks[-1][1]
		else:
			self.min_task_point = 0

	def _set_max_users_point(self):
		"""
		Set maximum task point

		:return: None
		"""
		self.max_users_point = self.users[0][1]
		logger.debug('Maximum user points: %d', self.max_users_point)

	def _set_initial_config(self):
		"""
		Function set initial configuration

		:return: None
		"""		
		self._set_users_number()
		self._set_tasks_number()
		self._set_min_task_point()
		self._set_max_users_point()

		logger.debug('Tasks number: %d', self.tasks_number)
		logger.debug('Minimum points of tasks: %d', self.min_task_point)
		# Set max remain user points equal max users point
		self.max_remain_user_point = self.max_users_point

	def spare_complex_task(self):
		"""
		From tasks create:
		1. complex_tasks -> set() - if it in task
		2. remain_tasks -> set() - all tasks left
		3. update tasks
		"""
		counter = 0
		for name, value in self.tasks:
			if value > self.max_users_point:
				counter += 1
				self.complex_tasks.add(name)
			else:
				self.remain_tasks.add(name)

		self.tasks = self.tasks[counter:]

		self._set_tasks_number()

	def remain_usr_points(self):
		"""
		This functions adding to the list of users `remain_points`
		--------------------------------------------------
		Ex. [User_name, point, remain_point]
		--------------------------------------------------
		:return: None
		"""
		for n in self.users:
			n.append(self.data['users'][n[0]]['remain_points'])
		logger.debug('`remain_point` was successfully added to users list.')

	def _set_max_remain_user_point(self):
		"""
		Function find and set maximum of remain points of users
		It's need for exit from while loop in `task_allocator`
		--------------------------------------------------
		Ex. [User_name, point, remain_point]
		`self.max_remain_user_point` -> remain_point
		--------------------------------------------------
		:return: None
		"""
		self.max_remain_user_point = max(self.users, key=lambda x: x[2])[2]
		logger.debug('Maximum of remain points of users: %d', self.max_remain_user_point)

	def task_allocator(self):
		"""
		The main function that distributes tasks among users

		:return: none
		"""
		# run while tasks list not empty
		while self.tasks:
			# Set maximum of the remain point of users
			self._set_max_remain_user_point()
			# Then we check if `min_task_point` > `max_remain_user_point` -
			# exit from while loop
			if self.min_task_point > self.max_remain_user_point:
				break

			for n in range(self.users_number):
				# for every user find most suitable task
				# name -> users name
				# value -> users points
				# remains -> remain users points
				name, value, remains = self.users[n]

				for inx in range(self.tasks_number):
					# Find the task with max points which will satisfy the condition below
					# Give tasks to users if they have enough points
					if remains >= self.tasks[inx][1]:
						# create temp dict
						# task_inx -> {'Task': points}
						task_inx = {self.tasks[inx][0] : self.tasks[inx][1]}
						# Add task to data and `applied_tasks`
						self.data['users'][name]['tasks'].update(task_inx)
						self.applied_tasks.update(task_inx)

						# Change remain points in data[users][name] every time
						# when user takes the task.
						# And change `remain_points` in users list
						self.data['users'][name]['remain_points'] -= self.tasks[inx][1]
						self.users[n][2] = self.data['users'][name]['remain_points']

						# Then delete the used task from the tasks
						self.remain_tasks.remove(self.tasks[inx][0])
						del self.tasks[inx]
						# Finaly set number of tasks which left and min task point
						self._set_tasks_number()
						
						self._set_min_task_point()
						break
					else:
						continue

	def main_algorithm(self, show_plan=False, save_to_file=False):
		"""
		This function contains all functions from this module

		:return: None
		"""
		# First of all drop users task and sort data
		self.drop_users_tasks()
		self.sort_data_by_point()
		# Then we add `remain_points` to the list of users
		self.remain_usr_points()

		# We run algorithm in the "if" statements below if tasks
		# and users not empty
		if self.tasks and self.users:
			# setting users and tasks number,
			# min task and max users point
			self._set_initial_config()
			# Spare complex task
			self.spare_complex_task()
			# Run algorithm which distributes tasks among users
			self.task_allocator()
			self.log_debug_info()
		else:
			print_both_outputs("Your file doesn't have enough data. Please, fill it.",
				logging.WARNING)

		if show_plan:
			# Show detailed information
			self.show_user_plans()
		if save_to_file:
			# Rewrite JSON file with changes
			save_data_to_file(self.data)

	def log_debug_info(self):
		"""
		Log debug info to output logging file.
		"""
		logger.info('Applied tasks: %d', len(self.applied_tasks))
		logger.info('Remain tasks: %d', len(self.remain_tasks))
		logger.info('Complex tasks: %d', len(self.complex_tasks))

	def show_user_plans(self):
		"""
		Show detailed information about main_algorithm (assigned, complex,
        remain tasks) of users which was build by `task_allocator`

		:return: None
		"""
		for name, value, remains in self.users:
			user = self.data['users'][name]
			# calculate how is user is charged by work.
			efficiency = 1 - remains / user['points']
			# and set the efficiency to user
			self.set_users_efficiency(name, efficiency)
			print(consts.SHOW_USER_PLANS % (
				ConsoleColor.HEADER + name + ConsoleColor.WHITE,
				efficiency * 100,
				user['tasks'],
				value,
				remains
				))
		# in the end print conclusion
		self.print_conclusion()

	def set_users_efficiency(self, user, eff):
		"""
        Sets to global json data an efficiency work of user tasks.

        :param user: str -> user nickname
        :param eff: int -> % of efficiency work
        :return None
        """
		self.data['users'][user]['efficiency'] = eff
		logger.debug('The efficiency of work user %s is established.' % user)

	def print_conclusion(self):
		"""
		Function show conclusion
		"""
		print(consts.SHOW_CONCLUSION % (
			self.min_task_point,
			self.max_remain_user_point,
			self.remain_tasks,
			self.complex_tasks,
			self.applied_tasks))

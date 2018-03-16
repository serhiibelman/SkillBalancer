# Skill Balancer
Skill Balancer is a console application which distributes the right tasks for every user, so no one will stay 
without possible work. Users will get only tasks that they could deal with their level(points).

### Requirements ####
- Python 3.5

### Algorithm ###

1. Skill Balancer gets a dict with users and tasks data from json file.
    
2. Sort both dicts (users, tasks) in reversed mode (from bigger points to lower points).
    
3. Add tasks to the `complex_tasks` value if their points are bigger than an user with max points.
       
4. Check if tasks and users dicts have at least 1 user and 1 task.
     
5. Start a loop which will work while any task can be assigned to user. 
    
6. Go through every task (from heavy to easy) and check users (from senior to junior user level). Also skip tasks, which are in `complex_tasks` value.
       
7. If user can afford task (user have enough points for task points), then user points will be decreased by task points.
       
8. When user was assigned by some task he wouldn't join to assigning task loop again. This needs for an effectively distributing a task at first time. So no one wil stay without task if task can be assigned.
       
9. Skill balancer checks if any user can let one of remain tasks. Quit loop if not. 
       
10. After first loop has ended then data will be unsorted, but TB won't sort it again. He would start to assign tasks again while condition (step 5) says True. So now dict with users has scattered items which TB would fill with remain tasks.
            

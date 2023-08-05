Task-Tracker -- A simple command line project task tracking tool
https://launchpad.net/tasks-tracker | http://www.softwebia.com
Developed by: Mohamed Diarra <moh@softwebia.com> | http://moh.softwebia.com

Usage: tasks: [-n TASK] 

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -R, --recursive       run commands recursively in subfolders

  Setup commands:
    --init              initialize tasks in folder
    --un-init           un-initialize tasks for current folder (Removes .tasks
                        file).
    --reset             initialize new tasks in folder, loses all previous
                        tasks
    --empty-trash       permanently delete tasks in trash
    --archive           move all completed tasks to trash

  Basic tasks commands:
    -n NEW, --new=NEW   create a new task
    -c, --completed     set a task as completed
    -d, --delete        move a task to the trash
    -a, --active        set a task as active

  List commands:
    --indexed           show index when listing tasks
    --detail            show more details when listing tasks
    -C, --show-completed
                        show only completed tasks
    -D, --show-deleted  show trashed tasks
    -A, --show-all      show all tasks (active, completed and trashed)
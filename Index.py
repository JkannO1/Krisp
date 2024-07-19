import json
import os
import time

tasks_file = 'tasks.json'

def load_tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as file:
            return json.load(file)
    return {}

def save_tasks(tasks):
    with open(tasks_file, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, task_name, parent_id=None):
    task_id = str(len(tasks) + 1)
    new_task = {
        'name': task_name,
        'subtasks': {},
        'parent_id': parent_id,
        'start_time': None,
        'elapsed_time': 0
    }
    tasks[task_id] = new_task
    if parent_id:
        tasks[parent_id]['subtasks'][task_id] = new_task
    save_tasks(tasks)

def list_tasks(tasks, parent_id=None, level=0):
    for task_id, task in tasks.items():
        if task['parent_id'] == parent_id:
            print('  ' * level + f"{task_id}. {task['name']} (Elapsed Time: {task['elapsed_time']}s)")
            list_tasks(task['subtasks'], task_id, level + 1)

def edit_task(tasks, task_id, new_name):
    if task_id in tasks:
        tasks[task_id]['name'] = new_name
        save_tasks(tasks)

def delete_task(tasks, task_id):
    if task_id in tasks:
        parent_id = tasks[task_id]['parent_id']
        if parent_id:
            del tasks[parent_id]['subtasks'][task_id]
        del tasks[task_id]
        save_tasks(tasks)

def start_task(tasks, task_id):
    if task_id in tasks:
        tasks[task_id]['start_time'] = time.time()
        save_tasks(tasks)

def stop_task(tasks, task_id):
    if task_id in tasks and tasks[task_id]['start_time']:
        elapsed_time = time.time() - tasks[task_id]['start_time']
        tasks[task_id]['elapsed_time'] += round(elapsed_time, 1)  # Round off the elapsed time to 1 decimal place
        tasks[task_id]['start_time'] = None
        save_tasks(tasks)
        list_ongoing_timers(tasks)  # Display currently ongoing timers after stopping a task

def list_ongoing_timers(tasks):
    print("")
    for task_id, task in tasks.items():
        if task['start_time'] is not None:
            print(f"{task_id}. {task['name']} (Started at: {time.ctime(task['start_time'])})")
        list_ongoing_timers(task['subtasks'])

def main():
    tasks = load_tasks()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nCurrent Tasks:")
        list_tasks(tasks)
        list_ongoing_timers(tasks)
        print("\nCommands: add, list, edit, delete, start, stop, quit")
        command = input("Enter command: ").strip().lower()
        if command == 'add':
            task_name = input("Enter task name: ").strip()
            parent_id = input("Enter parent task ID (or leave blank for top-level task): ").strip() or None
            add_task(tasks, task_name, parent_id)
        elif command == 'list':
            list_tasks(tasks)
            input("\nPress Enter to continue...")
        elif command == 'edit':
            task_id = input("Enter task ID to edit: ").strip()
            new_name = input("Enter new task name: ").strip()
            edit_task(tasks, task_id, new_name)
        elif command == 'delete':
            task_id = input("Enter task ID to delete: ").strip()
            delete_task(tasks, task_id)
        elif command == 'start':
            task_id = input("Enter task ID to start: ").strip()
            start_task(tasks, task_id)
        elif command == 'stop':
            task_id = input("Enter task ID to stop: ").strip()
            stop_task(tasks, task_id)
        elif command == 'quit':
            break
        else:
            print("Unknown command. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
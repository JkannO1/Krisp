import json
import os
import time
from datetime import datetime
from colorama import Fore, Back, Style

tasks_file = 'tasks.json'
events_file = 'events.json'

def load_tasks():
    if os.path.exists(tasks_file):
        try:
            with open(tasks_file, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}
def save_tasks(tasks):
    with open(tasks_file, 'w') as file:
        json.dump(tasks, file, indent=4)

def load_events():
    if os.path.exists(events_file):
        try:
            with open(events_file, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def save_events(events):
    with open(events_file, 'w') as file:
        json.dump(events, file, indent=4)

def add_task(tasks, task_name, parent_id=None, due_date=None, priority=0):
    task_id = str(len(tasks) + 1)
    new_task = {
        'name': task_name,
        'subtasks': {},
        'parent_id': parent_id,
        'start_time': None,
        'elapsed_time': 0,
        'due_date': due_date,
        'priority': priority
    }
    tasks[task_id] = new_task
    if parent_id:
        tasks[parent_id]['subtasks'][task_id] = new_task
    save_tasks(tasks)

def add_event(events, event_name, event_date):
    if event_date not in events:
        events[event_date] = []
    events[event_date].append(event_name)
    save_events(events)

def display_calendar(events):
    print(f"\n{Fore.YELLOW}Calendar View:{Fore.WHITE}")
    for event_date, event_list in sorted(events.items()):
        print(f"{Fore.RED}{event_date}{Fore.WHITE}:")
        for event in event_list:
            print(f"  - {event}")
    input("Press Enter to continue...")

def display_calendar1(events):
    print(f"\n{Fore.YELLOW}Calendar View:{Fore.WHITE}")
    for event_date, event_list in sorted(events.items()):
        print(f"{Fore.RED}{event_date}{Fore.WHITE}:")
        for event in event_list:
            print(f"  - {event}")

def edit_task(tasks, task_id, new_name):
    if task_id in tasks:
        tasks[task_id]['name'] = new_name
        save_tasks(tasks)
    else:
        print(f"Error: Task ID {task_id} not found.")
 
def delete_task(tasks, task_id):
    if task_id in tasks:
        parent_id = tasks[task_id]['parent_id']
        if parent_id:
            del tasks[parent_id]['subtasks'][task_id]
        del tasks[task_id]
        save_tasks(tasks)
    else:
        print(f"Error: Task ID {task_id} not found.")

def start_task(tasks, task_id):
    if task_id in tasks:
        tasks[task_id]['start_time'] = time.time()
        save_tasks(tasks)
    else:
        print(f"Error: Task ID {task_id} not found.")

def stop_task(tasks, task_id):
    if task_id in tasks:
        if tasks[task_id]['start_time']:
            elapsed_time = time.time() - tasks[task_id]['start_time']
            tasks[task_id]['elapsed_time'] += round(elapsed_time, 1)  # Round off the elapsed time to 1 decimal place
            tasks[task_id]['start_time'] = None
            save_tasks(tasks)
            list_ongoing_timers(tasks)  # Display currently ongoing timers after stopping a task
        else:
            print(f"Error: Task ID {task_id} is not currently running.")
    else:
        print(f"Error: Task ID {task_id} not found.")

def list_tasks(tasks, parent_id=None, level=0):
    for task_id, task in tasks.items():
        if task['parent_id'] == parent_id:
            elapsed_hours = task['elapsed_time'] / 3600  # Convert seconds to hours
            print('  ' * level + f"{task_id}. {Fore.RED}{task['name']}{Fore.WHITE} (Elapsed Time: {Fore.RED}{elapsed_hours:.2f}h{Fore.WHITE})")
            list_tasks(task['subtasks'], task_id, level + 1)

def list_ongoing_timers(tasks):
    ongoing = False
    for task_id, task in tasks.items():
        if task['start_time'] is not None:
            if not ongoing:
                print(f"\n{Fore.YELLOW}Ongoing Timers:{Fore.WHITE}")
                ongoing = True
            print(f"{task_id}. {Fore.RED}{task['name']}{Fore.WHITE} (Started at: {time.ctime(task['start_time'])})")
        if list_ongoing_timers(task['subtasks']):
            ongoing = True
    return ongoing

def main():
    if not os.path.exists(tasks_file):
        with open(tasks_file, 'w') as file:
            json.dump({}, file)
    if not os.path.exists(events_file):
        with open(events_file, 'w') as file:
            json.dump({}, file)

    tasks = load_tasks()
    events = load_events()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.YELLOW}Current Tasks:{Fore.WHITE}")
        list_tasks(tasks)
        if not list_ongoing_timers(tasks):
            print(f"\n{Fore.YELLOW}Ongoing Timers:{Fore.WHITE}\nNone")
        display_calendar1(events)
        print(f"\n{Fore.YELLOW}Commands:{Fore.WHITE}")
        print("add_task, add_event, list, edit, delete, start, stop, calendar, quit")
        command = input(f"{Fore.GREEN}Enter command: {Fore.WHITE}").strip().lower()
        if command == 'add_task':
            task_name = input("Enter task name: ").strip()
            parent_id = input("Enter parent task ID (or leave blank for top-level task): ").strip() or None
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip() or None
            try:
                priority = int(input("Enter priority (0-5, where 5 is highest): ").strip() or 0)
                if priority < 0 or priority > 5:
                    raise ValueError
            except ValueError:
                print("Invalid priority. Please enter a number between 0 and 5.")
                continue
            add_task(tasks, task_name, parent_id, due_date, priority)
        elif command == 'add_event':
            event_name = input("Enter event name: ").strip()
            event_date = input("Enter event date (YYYY-MM-DD): ").strip()
            add_event(events, event_name, event_date)
        elif command == 'calendar':
            display_calendar(events)
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
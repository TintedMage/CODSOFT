import json
import os
import platform

DATA_FOLDER = 'data'
PENDING_TASKS_FILE = os.path.join(DATA_FOLDER, 'pending_tasks.json')
COMPLETED_TASKS_FILE = os.path.join(DATA_FOLDER, 'completed_tasks.json')
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    
def load_tasks(file_path):
    """Load tasks from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_tasks(file_path, tasks):
    """Save tasks to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)

def clear_screen():
    """Clear the console screen based on the operating system."""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def display_tasks(tasks, start_index=0, tasks_per_page=5, show_all=False):
    """Display a paginated list of tasks or all tasks."""
    clear_screen()
    print("To-do list app by Khushal\n")
    print("Tasks: Pending")
    print("----------------------------------")
    
    if show_all:
        for n, task in enumerate(tasks, start=1):
            print(f"{n}. {task['name']}")
            print(f"   {task['sub_content'][:15]}")  # Truncated to 15 characters
            print("----------------------------------")
        print("Showing all tasks. Press 'n' to go back to the first 5 tasks.")
    else:
        end_index = start_index + tasks_per_page
        for n, task in enumerate(tasks[start_index:end_index], start=start_index+1):
            print(f"{n}. {task['name']}")
            print(f"   {task['sub_content'][:15]}")  # Truncated to 15 characters
            print("----------------------------------")
        print(f"Showing {min(len(tasks), end_index)}/{len(tasks)} tasks.")
        print("Press 'n' for next 5 tasks, 'p' for previous 5 tasks, 'v' to view all tasks.")

def add_task(tasks):
    """Add a new task to the list."""
    task_name = input("Enter task name: ")
    sub_content = input("Enter sub content: ")
    new_task = {'name': task_name, 'sub_content': sub_content}
    tasks.append(new_task)
    save_tasks(PENDING_TASKS_FILE, tasks)

def edit_task(tasks, task_number):
    """Edit an existing task."""
    if 0 <= task_number < len(tasks):
        task = tasks[task_number]
        print(f"Editing Task: {task['name']}")
        new_name = input("Enter new task name (leave blank to keep current): ")
        if new_name:
            task['name'] = new_name
        new_sub_content = input("Enter new sub content (leave blank to keep current): ")
        if new_sub_content:
            task['sub_content'] = new_sub_content
        save_tasks(PENDING_TASKS_FILE, tasks)
    else:
        print("Invalid task number")

def mark_task_completed(tasks, completed_tasks, task_number):
    """Mark a task as completed and move it to the completed tasks list."""
    if 0 <= task_number < len(tasks):
        completed_task = tasks.pop(task_number)
        completed_tasks.append(completed_task)
        save_tasks(PENDING_TASKS_FILE, tasks)
        save_tasks(COMPLETED_TASKS_FILE, completed_tasks)
    else:
        print("Invalid task number")

def view_completed_tasks(completed_tasks):
    """Display the list of completed tasks."""
    clear_screen()
    print("Tasks: Completed")
    print("----------------------------------")
    for n, task in enumerate(completed_tasks, start=1):
        print(f"{n}. {task['name']}")
        print(f"   {task['sub_content'][:15]}")  # Truncated to 15 characters
        print("----------------------------------")
    input("Press Enter to return to pending tasks...")

def clear_completed_tasks(completed_tasks):
    """Clear all completed tasks."""
    completed_tasks.clear()
    save_tasks(COMPLETED_TASKS_FILE, completed_tasks)
    print("Completed tasks cleared")

def view_task(tasks, task_number):
    """View a single task."""
    clear_screen()
    if 0 <= task_number < len(tasks):
        task = tasks[task_number]
        print(f"Task: {task['name']}")
        print(f"Sub Content: {task['sub_content']}")
    else:
        print("Invalid task number")
    input("\nPress Enter to continue...")

def main():
    """Main function to run the task management CLI application."""
    pending_tasks = load_tasks(PENDING_TASKS_FILE)
    completed_tasks = load_tasks(COMPLETED_TASKS_FILE)
    tasks_per_page = 5
    start_index = 0
    show_all = False

    while True:
        if not show_all:
            display_tasks(pending_tasks, start_index, tasks_per_page, show_all)

        choice = input("\nEnter Task Number To Edit Respective Task or choose: \na: new task\t\t\tb: view completed task\nc: clear completed tasks\td: exit\n: ").strip().lower()

        if choice == 'a':
            add_task(pending_tasks)
            show_all = False
            start_index = 0
        elif choice == 'b':
            view_completed_tasks(completed_tasks)
        elif choice == 'c':
            clear_completed_tasks(completed_tasks)
        elif choice == 'd':
            break
        elif choice == 'v':
            show_all = True
            start_index = 0  # Reset to show all tasks
            display_tasks(pending_tasks, start_index, tasks_per_page, show_all)
        elif choice == 'n':
            if show_all:
                show_all = False
                start_index = 0  # Reset to show the first 5 tasks
                display_tasks(pending_tasks, start_index, tasks_per_page, show_all)
            else:
                if start_index + tasks_per_page < len(pending_tasks):
                    start_index += tasks_per_page
                    display_tasks(pending_tasks, start_index, tasks_per_page, show_all)
                else:
                    print("No more tasks to show.")
        elif choice == 'p':
            if not show_all:
                if start_index - tasks_per_page >= 0:
                    start_index -= tasks_per_page
                    display_tasks(pending_tasks, start_index, tasks_per_page, show_all)
                else:
                    print("No previous tasks to show.")
        elif choice.isdigit():
            task_number = int(choice) - 1
            action = input("Choose action:\nv: view task\ne: edit task\nc: mark task as completed\nChoice: ").strip().lower()
            if action == 'v':
                view_task(pending_tasks, task_number)
                # We do not reset start_index or show_all
            elif action == 'e':
                edit_task(pending_tasks, task_number)
            elif action == 'c':
                mark_task_completed(pending_tasks, completed_tasks, task_number)
            else:
                print("Invalid action")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

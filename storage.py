"""
Сохранение и загрузка задач
Версия 0.2.0
"""


def save_tasks(task_collection, name_file):
    with open(name_file, "w", encoding="utf-8") as file:
        for task in task_collection:
            line = task if task.endswith("\n") else task + "\n"
            file.write(line)


def load_tasks(name_file):
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            return [line for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        return []

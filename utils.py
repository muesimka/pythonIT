"""
Вспомогательные функции
Версия 0.2.0
"""
import sys
import os


def check_confirm(select_task, task_list):
    if select_task.isdigit():
        if 0 < int(select_task) <= len(task_list):
            return True
        print(f"Задачи с номером {select_task} нет в списке!")
        return False
    print("Введите именно номер задачи!")
    return False


def get_base_din():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.realpath(__file__))


def insure_saves_file(name_file):
    if not os.path.exists(name_file):
        with open(name_file, "w", encoding="utf-8") as f:
            f.write("")

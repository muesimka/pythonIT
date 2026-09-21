"""Основной файл приложения

    версия 0.0.6

    === Описание ===
        Приложение может сохранять задачи, выдает список задач, и может удалять и редактировать задачи

"""
from random import choice
import processes
import os

collection = []  # list of tasks
is_running = True


def show_collection(task_collection):
    print("=" * 45)
    for i, j in enumerate(task_collection):
        print(i + 1, j)
    print("=" * 45)


def show_menu():
    print("1 - Показать задачи \n"
          "2 - Добавить задачу \n"
          "3 - Редактировать задачи \n"
          "4 - Удаление задачи \n"
          "5 - Выход")


def check_confirm(select_task, task_list):
    if select_task.isdigit():
        if int(select_task) > 0 and int(select_task) <= len(task_list):
            return True
        else:
            print(f"Задачи с номером {select_task} нет в списке!")
            return False
    else:
        print(f"Введите именно номер задачи!")
        return False


def delete_tasks(task_collection):
    delete_task = input("Введите номер задачи: ")
    if check_confirm(delete_task, task_collection):
        task_collection.pop(int(delete_task) - 1)
        print(f"Задача {delete_task} удалена!")
    else:
        print("Неверный номер задачи!")


def edit_task(task_collection):
    edit_task = input("Введите номер задачи: ")
    if check_confirm(edit_task, task_collection):
        task_collection[int(edit_task) - 1] = input("Новое имя задачи: ")
    else:
        print("Неверный номер задачи!")


def add_task(task_collection):
    task_name = input("Введите имя задачи для добавления: ")
    if task_name.startswith(" "):
        if len(task_name) < 2:
            print("Название не может быть пустым")
        else:
            task_collection.append(f"Задача {len(task_collection) + 1}")
    else:
        task_collection.append(task_name)
        print(f"Задача {task_name} успешно добавлена!")


def main():
    global is_running
 
    name_file = 'saves.txt'
    if os.path.exists(name_file):
        with open(name_file, 'r', encoding='utf-8') as file:
            task_collection = [line.strip() for line in file if line.strip()]
    else:
        task_collection = []

    while is_running:
        show_menu()
        choice_user = input('Введите ваш выбор: ')

        match str(choice_user):
            case "1":
                show_collection(task_collection)
                input("нажмите ENTER для продолжения")

            case "2":
                add_task(task_collection)
                with open(name_file, 'w', encoding='utf-8') as file:
                    for task in task_collection:
                        file.write(task + "\n")

            case "3":
                show_collection(task_collection)
                edit_task(task_collection)
                with open(name_file, 'w', encoding='utf-8') as file:
                    for task in task_collection:
                        file.write(task + "\n")

            case "4":
                show_collection(task_collection)
                delete_tasks(task_collection)
                with open(name_file, 'w', encoding='utf-8') as file:
                    for task in task_collection:
                        file.write(task + "\n")

            case "5":
                is_running = False
                print("До свидиния!")

            case _:
                print('Такого пункта нет...')


if __name__ == '__main__':
    main()

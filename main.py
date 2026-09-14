"""Основной файл приложения Task Manager
    version 0.0.4
    -[x]
    приложение может сохранять задачи,
    редактировать, выдает список задач
    и может удалять задачу.
"""
collection = []
is_start = True


def show_collection(task_collection):
    print("=" * 30)
    for i, j in enumerate(task_collection):
        print(i + 1, j)
    print("=" * 30)

def show_menu():
    print('1 - показать задачи | 2 - добавить задачу | 3 - редактировать | 4 - удалить | 0 - выход')

while is_start:
    show_menu()
    choice_user = input('Введите ваш выбор: ')

    match str(choice_user):
        case '1':
            show_collection(collection)

        case '2':
            add_task = input("Введите имя задачи для добавления")
            collection.append(add_task)

        case '3':
            show_collection(collection)
            select_task = int(input("Введите номер задачи"))
            edit_task = input("Введите новое имя задачи для редактирования")
            collection[select_task - 1] = edit_task

        case '4':
            show_collection(collection)
            select_task = int(input("Введите номер задачи"))
            delete_task = input("Введите номер задачи для удаления")
            collection.pop(select_task - 1)

        case '0':
            is_start = False
            print('Выход')

        case _:
            print('Такого пункта нет')



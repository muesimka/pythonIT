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
            waite = input("Нажмите ENTER для продолжения")

        case '2':
            task_name = input("Введите имя задачи для добавления")
            if task_name.startswith(' '):
                if len(task_name) < 2 :
                    print("название не может быть пустым")
                    continue
                else:
                    print("название не может быть пустым")
            else:
                collection.append(f"задача {len(collection)} ")

        case '3':
            show_collection(collection)
            select_edit = input("Введите номер задачи")
            if int(select_edit.isdigit()):
                if (int(select_edit) > 0  and int(select_edit) <= len(collection)):
                    edit_name = input("новое имя задачи")
                    collection[int(select_edit) - 1] = edit_name
                    print(f"задача '{int(select_edit)}' : '{edit_name}' успешно отредактирована")
                else:
                    print("задачи с таким номером нет в списке")
            else:
                print("введеные данные должны быть номером списка задач")

        case '4':
            show_collection(collection)
            delete_edit = input("Введите номер задачи для удаления")
            if int(delete_edit) > 0  and delete_edit <= len(collection):
                collection.pop(delete_edit - 1)
                print(f"задача '{delete_edit}' успешно удалена")
            else:
                print("задачи с таким номером нет в списке")

        case '0':
            is_start = False
            print('Выход')

        case _:
            print('Такого пункта нет')



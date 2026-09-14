"""Основной файл приложения Task Manager
    version 0.0.3
    -[x] реализовать место хранения задач
    -[x] сделать функцию - показать задачи
    -[x] сделать функцию - добавить задачу
    -[x] сделать функцию - редактировать задачу
    -[x] сделать функцию - удалить задачу
    -[x] реализовать выход
"""
collection = []  
is_start = True 

while is_start:
    print('1 - показать задачи | 2 - добавить задачу | 3 - редактировать | 4 - удалить | 0 - выход')
    choice_user = input('Введите ваш выбор: ')

    match str(choice_user):
        case '1':
            print(collection)

        case '2':
            task = input('Введите название задачи: ')
            collection.append(task)
            print(collection)

        case '3':
            print(collection)
            num = int(input('Введите номер задачи (с 0): '))
            new_name = input('Новое название: ')
            collection[num] = new_name
            print(collection)

        case '4':
            print(collection)
            num = int(input('Введите номер задачи (с 0): '))
            del collection[num]
            print(collection)

        case '0':
            is_start = False
            print('Выход')

        case _:
            print('Такого пункта нет')

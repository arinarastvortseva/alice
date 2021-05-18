import csv
""" Модуль для работы с csv-файлами"""
from itertools import cycle
"""Создать бесконечный итератор"""

with open('script-for-alice.csv', 'r', encoding='utf8') as csvfile:
    """ Читать сценарий, записанный в csv-файле"""
    data = csv.DictReader(csvfile, delimiter=';', quotechar=' ')
    events = {x['event']: [x['action'], x['branch'], x['image']] for x in data}


def handle_dialog(request, response, user_storage):
    """ Работать с диалогом

    Обрабатывает диалог
    Выводит сообщение Алисы, картинку и текст кнопок для продолжения игры
    В случае выбора кнопки 'конец игры' завершает сессию
    В случае выбора кнопки 'подождать еще день' вызывает первую ветку истории
    В случае выбора кнопки 'выбираться самой' вызывает вторую ветку истории
    Настраивает очередь сообщений из csv-файла и очередь картинок
    Возвращает ответ для пользователя"""

    if request.is_new_session:
        user_storage = {}
        response.set_text('Для завершения игры скажите "конец игры".\n')
        response.set_buttons([{'title': 'подождать еще день', 'hide': True},
                              {'title': 'выбираться самой', 'hide': True}])
        response.set_image('1030494/2e21639ad34cd97d8c9c', 'Милой Элитии исполнилось уже 20 лет, она стояла '
                                                           'у окна и рассматривала плывущие по небу облака.'
                                                           'Красавица думала про себя: '
                                                           '“Подождать мне еще один день или стоит уже '
                                                           'выбираться самой?'
                                                           'Для завершения игры скажите "конец игры".\n')
        return response, user_storage

    else:
        if request.command.lower() == 'конец игры':
            response.set_text('Спасибо за игру!\n' + 'До встречи!')
            response.set_end_session(True)
            user_storage = {}
            return response, user_storage

        elif request.command in ['подождать еще день']:
            user_storage = choose_branch('подождать еще день')
            user_storage, image, event = response_to_user()

            response.set_text(user_storage['event'])
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        elif request.command in ['выбираться самой']:
            user_storage = choose_branch('выбираться самой')
            user_storage, image, event = response_to_user()

            response.set_text(user_storage['event'])
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        elif request.command == user_storage['action']:
            user_storage, image, event = response_to_user()

            response.set_text(user_storage['event'])
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        response.set_text(user_storage['event'])
        return response, user_storage


def get_buttons(action):
    """ Функция для создания кнопок """
    actions = list(action)
    actions = ''.join(actions)
    buttons = [{'title': actions, 'hide': True}]
    return buttons


def choose_branch(branch):
    """ Функция выбора сюжета для ветки """
    a = []
    b = []
    for x in events.keys():
        if events[x][1] == branch:
            a.append(x)
            b.append(events[x][2])
    inf_list = cycle(a)
    image_list = cycle(b)
    user_storage = globals()
    user_storage['episodes'], user_storage['pictures'] = inf_list, image_list
    return user_storage


def response_to_user():
    """ Функция ответа пользователя"""
    user_storage = globals()
    event = next(user_storage['episodes'])
    action = events[event][0]
    image = events[event][2]
    buttons = get_buttons(action)

    user_storage['event'] = event
    user_storage['action'] = action
    user_storage['buttons'] = buttons
    return user_storage, image, event

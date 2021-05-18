import csv
from itertools import cycle

# Читаем сценарий, который находится в csv файле.
with open('script-for-alice.csv', 'r', encoding='utf8') as csvfile:
    data = csv.DictReader(csvfile, delimiter=';', quotechar=' ')
    # Названия элементов, к которым мы обращаемся в файле.
    events = {x['event']: [x['action'], x['branch'], x['image']] for x in data}


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    # Если начинается новая сессия, то игроку предлагается выбрать один из двух вариантов.
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
        # Обрабатываем ответ пользователя.
        # Если пользователь пищет конец игры, то сессия заканчивается.
        if request.command.lower() == 'конец игры':
            response.set_text('Спасибо за игру!\n' + 'До встречи!')
            response.set_end_session(True)
            user_storage = {}
            return response, user_storage

        # Пользователь выбрал первую ветку истории.
        elif request.command in ['подождать еще день']:
            # Создаём два массива.
            # В a заносится event.
            # В b заносится image.
            a = []
            b = []

            for x in events.keys():
                a.append(x)
                b.append(events[x][2])
            # Настраиваем очередь событий.
            inf_list = cycle(a)
            # Настраиваем очередь картинок.
            image_list = cycle(b)
            user_storage['questions'] = inf_list
            user_storage['pictures'] = image_list

            # Переход к следующему событию.
            event = next(user_storage['questions'])
            action = events[event][0]
            image = events[event][2]
            buttons = get_buttons(action)

            user_storage['event'] = event
            user_storage['action'] = action
            user_storage['buttons'] = buttons
            response.set_text(user_storage['event'])
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        # Пользователь выбрал вторую ветку истории.
        elif request.command in ['выбираться самой']:
            a = []
            b = []

            for x in events.keys():

                if events[x][1] == 'выбираться самой':
                    a.append(x)
                    b.append(events[x][2])

            inf_list = cycle(a)
            image_list = cycle(b)

            user_storage['questions'] = inf_list
            user_storage['pictures'] = image_list

            event = next(user_storage['questions'])

            action = events[event][0]
            image = events[event][2]
            buttons = get_buttons(action)

            user_storage['event'] = event
            user_storage['action'] = action
            user_storage['buttons'] = buttons
            response.set_text(user_storage['event'])
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        # Выбираем действие.
        elif request.command == user_storage['action']:
            # Пользователь выбрал что-то.
            event = next(user_storage['questions'])
            action = events[event][0]
            image = events[event][2]
            buttons = get_buttons(action)
            user_storage['event'] = event
            user_storage['action'] = action
            user_storage['buttons'] = buttons
            response.set_text(user_storage['event'])
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        response.set_text(user_storage['event'])
        return response, user_storage


# Функция для создания кнопок.
def get_buttons(action):
    actions = list(action)
    actions = ''.join(actions)

    buttons = [{'title': actions, 'hide': True}]
    return buttons

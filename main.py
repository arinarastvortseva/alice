import csv
from itertools import cycle


with open('script-for-alice.csv', 'r', encoding='utf8') as csvfile:
    data = csv.DictReader(csvfile, delimiter=';', quotechar=' ')
    events = {x['event']: [x['action'], x['branch'], x['image']] for x in data}


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):

    if request.is_new_session:
        user_storage = {}
        response.set_text('объяснялочка что здесь происходит и начало, чтобы уже можно было выбрат разветвление!'
                          'Для завершения игры скажите "конец игры".\n')
        response.set_buttons([{'title': 'branch 1', 'hide': True},
                             {'title': 'branch 2', 'hide': True}])
        return response, user_storage

    else:
        # Обрабатываем ответ пользователя.
        if request.command.lower() == 'конец игры':
            response.set_text('Спасибо за игру!\n' + 'До встречи!')
            response.set_end_session(True)
            user_storage = {}

            return response, user_storage

        elif request.command.lower() in ['branch 1']:
            a = []
            b = []

            for x in events.keys():
                a.append(x)
                b.append(events[x][2])

            inf_list = cycle(a)
            image_list = cycle(b)
            print(b)
            user_storage['questions'] = inf_list
            user_storage['pictures'] = image_list

            event = next(user_storage['questions'])
            # image = next(user_storage['pictures'])
            action = events[event][0]
            image = events[event][2]
            buttons = get_buttons(action)

            user_storage['event'] = event
            user_storage['action'] = action
            user_storage['buttons'] = buttons
            response.set_text(format(user_storage['event']))
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        elif request.command.lower() in ['branch 2']:
            a = []
            b = []
            print(events.keys())
            for x in events.keys():
                print(events[x][1])
                if events[x][1] == 'branch 2':
                    a.append(x)
                    b.append(events[x][2])
            print(a)
            print(b)
            inf_list = cycle(a)
            image_list = cycle(b)
            print(b)
            user_storage['questions'] = inf_list
            user_storage['pictures'] = image_list

            event = next(user_storage['questions'])
            # image = next(user_storage['pictures'])
            action = events[event][0]
            image = events[event][2]
            buttons = get_buttons(action)

            user_storage['event'] = event
            user_storage['action'] = action
            user_storage['buttons'] = buttons
            response.set_text(format(user_storage['event']))
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage

        elif request.command.lower() == user_storage['action']:
            # Пользователь выбрал что-то.
            event = next(user_storage['questions'])
            action = events[event][0]
            image = events[event][2]
            buttons = get_buttons(action)
            user_storage['event'] = event
            user_storage['action'] = action
            user_storage['buttons'] = buttons
            response.set_text(format(user_storage['event']))
            response.set_buttons(user_storage['buttons'])
            response.set_image(image, event)
            return response, user_storage
        # buttons = get_buttons(user_storage['action'])
        # response.set_buttons(buttons)
        response.set_text(format(user_storage['event']))
        return response, user_storage


def get_buttons(action):
    actions = list(action)
    actions = ''.join(actions)

    buttons = [{'title': actions, 'hide': True}]
    return buttons


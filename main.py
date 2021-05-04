# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:

        response.set_text('Вход: объясняловка, что вообще происходит и как жить дальше. Предложение поиграть.')
        response.set_buttons([{'title': 'я хочу играть!', 'hide': True}, {'title': 'помощь', 'hide': True},
                             {'title': 'выход', 'hide': True}])

        return response, user_storage
    else:
        # Обрабатываем ответ пользователя.
        if request.command.lower() == "выход":
            response.set_text("Спасибо за игру!\n Надеюсь тебе понравилось!")
            response.set_end_session(True)
            user_storage = {}

            return response, user_storage

        elif request.command.lower() == 'помощь':
            response.set_text('Шаг1: идёт жалобная история про Элитию. Предлагается 2 варианта развития событий\n'
                              'Для завершения игры скажите "конец игры".\n')
            response.set_buttons([{'title': 'вариант 1', 'hide': True}, {'title': 'вариант2', 'hide': True},
                                  {'title': 'помощь', 'hide': True}])
            user_storage = {}
            return response, user_storage

        elif response.command.lower() == 'вариант 1':

            response.set_text("Шаг 2.1\n Подождать еще один день и быть спасенной принцем. Ура!")
            response.set_buttons([{'title': 'приготовиться быть спасенной', 'hide': True}])

            user_storage = {}
            return response, user_storage


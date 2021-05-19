# Игра для Яндекс Алисы “Путь истины”
![логотип](https://github.com/daria-riumkina/alice/blob/main/Лого.png?raw=true)
## Описание программы

Интерактивный квест про принцессу Элитию, которая решает выбраться из заточения в замке. Игра встроена в Яндекс Алису и подходит для всей семьи!

Игрок проходит вместе с принцессой путь, помогая ей побеждать драконов, знакомиться с людьми и искать себе новый дом с помощью возможности сделать выбор за Элитию.

## Требования:
Наличие Яндекс Алисы на экране телефона или компьютера (игра не адаптируется под колонку и другие умные устройства без экрана)

## Как играть?
Вам необходимо подключиться к Алисе с утройства, имеющего экран и набрать команду "Запусти навык Путь истины"
![подключение](https://github.com/zaitsevayulia/alice/blob/main/2021-05-19%20(3).png?raw=true)

А затем читать историю и выбрать, каким путем идти принцессе!

## Как работает программа?
Код написан полностью на языке Python, пример кода ниже:
```
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
```

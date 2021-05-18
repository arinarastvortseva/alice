import json
"""Модуль для работы с форматом JSON"""


class AliceRequest(object):

    """ Класс AliceRequest используется для реализации удобного интерфейса для взаимодействия с запросом Алисы.

    Основное применение: удобное предоставление доступа к компонентам запроса пользователя Алисы.

    Атрибуты
    ----------
    request_dict:request_dict

    Методы
    ----------
    version()
        возвращает текущую версию Алисы.
    session()
        возвращает текущую сессию пользователя.
    user_id()
        возвращает user_id пользователя, который отправил запрос.
    is_new_session()
        возвращает данные о сессии.
    command()
        ответ от пользователя.
    """

    def __init__(self, request_dict):
        self._request_dict = request_dict

    @property
    def version(self):
        """ Данные о версии Алисы.
        :return: текущая версия Алисы.
        """
        return self._request_dict['version']

    @property
    def session(self):
        """ Данные о текущей сессии.
        :return: текущая сессия пользователя."""
        return self._request_dict['session']

    @property
    def user_id(self):
        """Данные о пользователе.
        :return: user_id пользователя."""
        return self.session['user_id']

    @property
    def is_new_session(self):
        """Данные о сессии.
        :return:True, если пользователь только начал диалог, иначе False."""
        return bool(self.session['new'])

    @property
    def command(self):
        """ Ответ от пользователя
        :return: ответ от пользователя
        """
        return self._request_dict['request']['command']

    def __str__(self):
        """ Отвечает за строковое представления объекта
        :return: строку
        """
        return str(self._request_dict)


class AliceResponse(object):

    """ Класс AliceResponse предназначен для реализации удобного интерфейса взаимодействия с ответом Алисы.

    Основное применение:предоставление удобного доступа к компонентам ответа Алисы.

    Атрибуты
    ---------
    _response_dict
    принимает аргументы класса AliceRequest для установки версии и сессии для ответа.

    Методы
    ---------
    set_text()
        задаёт ответ Алисы в текстовом формате.
    set_buttons()
        прикрепляет варианты ответа пользователя(кнопки).
    set_end_session()
        закрывает сессию с пользователем.
    set_image()
        прикрепляет картинку к ответу.

    """

    def __init__(self, alice_request):
        self._response_dict = {
            'version': alice_request.version,
            'session': alice_request.session,
            'response': {
                "end_session": False
            }
        }

    def dumps(self):
        """Функция dumps() модуля json сериализирует объект Python obj в строку str формата JSON
        :return: строка str формата JSON
        """
        return json.dumps(
            self._response_dict,
            ensure_ascii=False,
            indent=2
        )

    def set_text(self, text):
        """ Текст Алисы
        :param text: то, что выводится в ответ на действие пользователя
        :return: ответ Алисы в текстовом формате.
        """
        self._response_dict['response']['text'] = text[:1024]

    def set_buttons(self, buttons):
        """Прикрепляет кнопки
        :param buttons: на кнопке выводится действие(action)
        :return: кнопки с текстом
        """
        self._response_dict['response']['buttons'] = buttons

    def set_end_session(self, flag):
        """ Закрытие сессии
        :param flag:передаёт закрывается сессия или нет
        :return: True, если заканчивается сессию, иначе False
        """
        self._response_dict['response']['end_session'] = flag

    def set_image(self, image, event):
        """ Прикрепление картинки к тексту
        :param image: передаёт id картинки
        :param event: передаёт описание сюжета
        :return: Картинка
        """
        self._response_dict['response']['card'] = {}
        self._response_dict['response']['card']['type'] = 'BigImage'
        self._response_dict['response']['card']['description'] = event
        self._response_dict['response']['card']['image_id'] = image

    def __str__(self):
        """ Отвечает за строковое представления объекта
        :return: строка
        """
        return self.dumps()

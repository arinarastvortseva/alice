import logging
""" Модули для работы с логами"""
from alice_sdk import AliceRequest, AliceResponse
"""Модуль для работы с API Алисы"""
from main import handle_dialog
"""Модуль с логикой игры"""
from flask import Flask, request
app = Flask(__name__)
"""Подмодули Flask для запуска веб-сервиса."""
logging.basicConfig(level=logging.DEBUG)

session_storage = {}


@app.route('/alice', methods=['POST'])
def main():
    """ Функция получает тело запроса и возвращает ответ

    :return: ответ
    """
    alice_request = AliceRequest(request.json)
    logging.info('Request: {}'.format(alice_request))
    alice_response = AliceResponse(alice_request)
    user_id = alice_request.user_id
    alice_response, session_storage[user_id] = handle_dialog(
        alice_request, alice_response, session_storage.get(user_id)
    )
    logging.info('Response: {}'.format(alice_response))
    return alice_response.dumps()


app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, request

app = Flask(__name__)

@app.route('/alice', methods=['POST'])
def resp():
    text = request.json.get('request', {}).get('command')

    end = False

    if text == 'выход':
        response_text = 'Всего хорошего! Приходите позже, мы вас ждём!'
        end = True
    elif text:
        response_text = 'Жили были трали вали тут должен быть сценарий'
    else:
        response_text = 'Добро пожаловать в игровой навык, который еще не разработан! Надеюсь еще не дедлайн!!!!!'

    response = {
        'response': {
            'text': response_text,
            "card": {
                "type": "BigImage",
                "image_id": "965417/f8b5c546452c24dd1e44",
                "title": "Супер пупер мега квест",
                "description": "тут должно быть краткое описание что вообще происходит мрпсрачрачпяпвя",

            },
            'end_session': end,
            'buttons': [
                {'title': 'Я хочу начать игру!', 'hide': True},
                {'title': 'выход', 'hide': True},
            ]
        },
        'version': '1.0'
    }
    return response


app.run('0.0.0.0', port=5000, debug=True)
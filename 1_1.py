import requests
import yaml

def get_access_token(client_id, client_secret):
    url = "https://stepik.org/oauth2/token"
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, json=data)
    return response.json()['access_token']

def update_step_text(step_id, new_text, token):
    url = f'https://stepik.org/api/steps/{step_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'step': {
            'id': step_id,
            'content': new_text
        }
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

# Загружаем учетные данные с явным указанием кодировки
with open('creds.yaml', 'r', encoding='utf-8') as file:
    creds = yaml.safe_load(file)

client_id = creds['client_id']
client_secret = creds['client_secret']

# Получаем токен
token = get_access_token(client_id, client_secret)

# Новый текст урока
step_id = 1.1  # Замените на фактический ID вашего шага
new_text = {
    'step': {
        'content': {
            'title': 'Пример сложения',
            'text': (
                'Давайте рассмотрим простой пример сложения двумя числами. '
                'Если у вас есть 1 яблоко и вы получите еще 1, то у вас теперь будет два яблока. '
                'Это можно записать как:\n\n'
                '1 + 1 = 2\n\n'
                'Сложение — это операция, которая позволяет нам собирать количество. '
                'Когда мы складываем два числа, мы ищем итоговое количество, '
                'которое получается из их объединения.'
            ),
        },
        'lesson': 'lesson_id',  # Укажите корректный ID урока
        'position': 1
    }
}

# Обновляем текст шага
result = update_step_text(step_id, new_text, token)

# Проверяем результат
if 'step' in result:
    print("Содержимое шага обновлено успешно.")
else:
    print("Ошибка при обновлении шага:", result)
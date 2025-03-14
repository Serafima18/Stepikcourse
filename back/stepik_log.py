import requests

url = 'https://stepik.org/api/authorize'
username = 'ta.ko1@mail.ru'
password = ''

response = requests.post(url, data={'email': username, 'password': password})

if response.status_code == 200:
    token = response.json().get('token')
    print('Успешный логин. Ваш токен:', token)
else:
    print('Ошибка логина:', response.json())

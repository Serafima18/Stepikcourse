import requests
import yaml

# Чтение учетных данных из creds.yaml
with open('creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

client_id = creds['client_id']
client_secret = creds['client_secret']

# URL для получения токена
token_url = "https://stepik.org/oauth2/token"

# Подготовка данных для запроса
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

# Выполнение запроса
response = requests.post(token_url, data=data)

if response.status_code == 200:
    token = response.json()['access_token']
    print("Токен получен:", token)
else:
    print("Ошибка при получении токена:", response.status_code, response.text)
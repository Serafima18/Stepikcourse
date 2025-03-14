import requests
import yaml
import csv

with open('creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

client_id = creds['client_id']
client_secret = creds['client_secret']
redirect_uri = 'https://stepik.org/course/234353/syllabus'
authorize_url = f'https://stepik.org/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}'

print(f'URL для авторизации: {authorize_url}')

# Когда я перехожу по ссылке, в адресной строке вместо кода написано error=unauthorized_client

received_code = input('Код: ')

token_url = 'https://stepik.org/oauth2/token'

data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'code': received_code,
}

response = requests.post(token_url, data=data)
token_info = response.json()

my_token = token_info.get('my_token')

data_course = []

with open('course-234353-dump.csv', mode='r', encoding='latin1') as csvfile: # utf-8 выскакивает ошибка
    reader = csv.reader(csvfile)
    for row in reader:
        data_course.append(row)

url = 'https://stepik.org/api/step-texts/{}'.format(data_course[-2][1])
headers = {'Authorization': 'Bearer {}'.format(my_token)}
data = {'step_text': {'text': 'Новый текст'}}

response = requests.put(url, headers=headers, json=data)
print(response.json())

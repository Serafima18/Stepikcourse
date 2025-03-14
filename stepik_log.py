import requests
import yaml
import csv

with open('creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

client_id = creds['client_id']
client_secret = creds['client_secret']
api_host = 'https://stepik.org'

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('{}/oauth2/token/'.format(api_host),
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
my_token = response.json().get('access_token', None)  # до сюда вроде все хорошо

data_course = []

with open('course-234353-dump.csv', mode='r', encoding='latin1') as csvfile:  # utf-8 выскакивает ошибка
    reader = csv.reader(csvfile)
    for row in reader:
        data_course.append(row)

url = 'https://stepik.org/api/step-texts/{}'.format(data_course[-2][1])
headers = {'Authorization': 'Bearer {}'.format(my_token)}
data = {'step_text': {'text': 'Новый текст'}}

response = requests.put(url, headers=headers, json=data)
print(response.json())

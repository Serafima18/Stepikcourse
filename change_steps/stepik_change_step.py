import requests
import yaml
from get_steps_id import _steps_id, get_token


def update_step(step_id, token, txt):
    url = f'https://stepik.org/api/steps/{step_id}'
    headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
    data = {'step': {'text': txt}}
    response = requests.patch(url, headers=headers, json=data)  # ругается на put, patch и post
    print(response.status_code)
    print(response.json())


with open('../creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

my_token = get_token(creds['client_id'], creds['client_secret'], 'https://stepik.org')
steps_id = _steps_id()

new_text = 'new text'

update_step(steps_id[0], my_token, new_text)

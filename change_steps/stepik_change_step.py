import requests
import yaml
from get_steps_id import _steps_id, get_token


def update_step(step_id, token, txt):
    url = f'https://stepik.org/api/step-sources/{step_id}'
    headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
    data = {
        'step-source': {
            'id': step_id,
            'block': {
                'name': 'text',
                'text': txt,
                'source': {'id': step_id},
                'is_html_enabled': True,
                'preserve_order': False
            },

            'lesson': 1659223,
            'position': 1
        }
    }

    response = requests.put(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())


with open('../creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

my_token = get_token(creds['client_id'], creds['client_secret'], 'https://stepik.org')
steps_id = _steps_id()

new_text = '''
new text
new text with some lines
eeeeeee'''

new_text_html = new_text.replace('\n', '<br>')

update_step(steps_id[0], my_token, new_text_html)

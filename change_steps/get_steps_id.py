import csv
import requests
import yaml


def get_token(client_id, client_secret, api):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    resp = requests.post(f'{api}/oauth2/token/',
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    return resp.json().get('access_token', None)


with open('../creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

api_host = 'https://stepik.org'

course_id = 234353

cross_domain = True

token = get_token(creds['client_id'], creds['client_secret'], api_host)


def fetch_object(obj_class, obj_id):
    api_url = f'{api_host}/api/{obj_class}s/{obj_id}'
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response[f'{obj_class}s'][0]


def fetch_objects(obj_class, obj_ids):
    objs = []

    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = f"{api_host}/api/{obj_class}s?{'&'.join(f'ids[]={obj_id}' for obj_id in obj_ids_slice)}"
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()
        objs += response[f'{obj_class}s']
    return objs


def _steps_id():
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    lessons_ids = [unit['lesson'] for unit in units]
    lessons = fetch_objects('lesson', lessons_ids)
    return [step for lesson in lessons for step in lesson['steps']]


step_ids = _steps_id()
csv_file = open(f'steps-{course_id}-dump.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerows([step_ids])
csv_file.close()

import requests

def update_step_text(step_id, new_text, token):
    url = f'https://stepik.org/lesson/1635418/step/{step_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'text': new_text
    }
    
    response = requests.put(url, json=data, headers=headers)
    
    print(f'Response status code: {response.status_code}')
    if response.status_code == 200:
        print('Step updated successfully.')
        return response.json()  # Возвращаем ответ в формате JSON
    else:
        print('Failed to update step.')
        return None  # Вернем None в случае неудачи
import requests

def update_step_text(step_id, new_text, token):
    url = f'https://stepik.org/lesson/1635418/step/{step_id}'

import re
from requests.exceptions import HTTPError

def convert_to_choice_step(step_url, question, options, correct_option_index, token):
    """
    Преобразует существующий текстовый шаг в шаг с выбором ответа
    :param step_url: Полный URL шага (например, https://stepik.org/lesson/1635418/step/2)
    :param question: Текст вопроса (HTML)
    :param options: Список вариантов ответа
    :param correct_option_index: Индекс правильного ответа (с 0)
    :param token: API-токен
    """
    # Извлекаем ID урока и позицию шага
    match = re.search(r'lesson/(\d+)/step/(\d+)', step_url)
    if not match:
        raise ValueError("Неверный формат URL шага")
    
    lesson_id, step_pos = match.groups()
    
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
    
    try:
        # 1. Получаем текущий шаг
        response = requests.get(
            f'https://stepik.org/api/step-sources?lesson={lesson_id}&position={step_pos}',
            headers=headers
        )
        response.raise_for_status()
        step_data = response.json()
        
        if not step_data['step-sources']:
            raise ValueError("Шаг не найден")
            
        step_source = step_data['step-sources'][0]
        
        # 2. Формируем данные для преобразования в choice
        update_data = {
            'step-source': {
                'id': step_source['id'],
                'block': {
                    'name': 'choice',  # Меняем тип на choice
                    'text': question,
                    'options': [
                        {
                            'text': text,
                            'is_correct': (i == correct_option_index),
                            'feedback': 'Верно!' if i == correct_option_index else 'Неверно',
                            'hint': ''
                        } for i, text in enumerate(options)
                    ],
                    'source': {'id': step_source['id']},
                    'is_html_enabled': True,
                    'is_multiple_choice': False,
                    'sample_size': 0,
                    'preserve_order': False
                },
                'lesson': int(lesson_id),
                'position': int(step_pos)
            }
        }
        
        # 3. Отправляем обновление
        response = requests.put(
            f'https://stepik.org/api/step-sources/{step_source["id"]}',
            json=update_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
        
    except HTTPError as e:
        print(f"Ошибка HTTP: {e.response.text if e.response else str(e)}")
        return None
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return None

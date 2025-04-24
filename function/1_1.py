import pytest
import requests
from unittest.mock import patch
from update_step_text.py import update_step_text

# Пример теста
def test_update_step_text_success():
    step_id = 1
    new_text = (
        '<h2>Пример сложения</h2>'
        '<p>Давайте рассмотрим простой пример сложения двух чисел. '
        'Если у вас есть 1 яблоко и вы получите еще 1, то у вас теперь будет два яблока. '
        'Это можно записать как:</p>'
        '<p>1 + 1 = 2</p>'
        '<p>Сложение — это операция, которая позволяет нам собирать количество. '
        'Когда мы складываем два числа, мы ищем итоговое количество, '
        'которое получается из их объединения.</p>'
    )
    token = "fake_token"
    
    url = f'https://stepik.org/lesson/1635418/step/{step_id}?unit=1657722'
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

    # Используем patch для мока requests.put
    with patch('requests.put') as mock_put:
        mock_response = mock_put.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'step': {'id': step_id, 'content': new_text}}

        result = update_step_text(step_id, new_text, token)

        # Проверяем, что requests.put был вызван с правильными параметрами
        mock_put.assert_called_once_with(url, json=data, headers=headers)

        # Проверяем, что результат правильный
        assert result['step']['id'] == step_id
        assert result['step']['content'] == new_text

    # Используем patch для мока requests.put
    with patch('requests.put') as mock_put:
        mock_response = mock_put.return_value
        mock_response.status_code = 404  # Симулируем ошибку
        mock_response.json.return_value = {'error': 'Step not found'}

        # Проверяем, что при вызове функции будет выброшено исключение
        with pytest.raises(requests.exceptions.HTTPError):
            update_step_text(step_id, new_text, token)

        # Проверяем, что requests.put был вызван
        mock_put.assert_called_once_with(url, json=data, headers=headers)
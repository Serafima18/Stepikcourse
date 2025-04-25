#!/usr/bin/env python3
"""
Скрипт для получения OAuth-токена Stepik API
"""

import requests
import yaml
from pathlib import Path

def get_stepik_token(client_id=None, client_secret=None):
    """
    Получает access token для API Stepik
    
    Args:
        client_id: Client ID приложения (если None, берет из creds.yaml)
        client_secret: Client Secret приложения (если None, берет из creds.yaml)
    
    Returns:
        str: Access token
    """
    # Если credentials не переданы, загружаем из файла
    if client_id is None or client_secret is None:
        try:
            creds_path = Path("creds.yaml")
            with open(creds_path, 'r') as f:
                creds = yaml.safe_load(f)
                client_id = creds["client_id"]
                client_secret = creds["client_secret"]
        except Exception as e:
            raise ValueError("Не удалось загрузить credentials. Укажите client_id и client_secret вручную или создайте creds.yaml") from e
    
    # Получаем токен
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(
        'https://stepik.org/oauth2/token/',
        data={'grant_type': 'client_credentials'},
        auth=auth
    )
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Токен успешно получен: {token}")
        return token
    else:
        error_msg = f"Ошибка получения токена: {response.status_code}\n{response.text}"
        print(error_msg)
        raise Exception(error_msg)

if __name__ == "__main__":
    try:
        token = get_stepik_token()
        # Можно сохранить токен в файл или переменную окружения
        # with open(".token", "w") as f:
        #     f.write(token)
    except Exception as e:
        print(f"Ошибка: {str(e)}")
import requests
import json


class InvalidToken(Exception):
    pass


def get_token(client_id: str, client_secret: str) -> str:
    """Получить токен доступа через секретки"""
    # 2. Get a token
    api_host = 'https://stepik.org'
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(
                        f'{api_host}/oauth2/token/',
                        data={'grant_type': 'client_credentials'},
                        auth=auth
                        )
    token = response.json().get('access_token', None)

    if not token:
        raise InvalidToken(
                'Невозможно авторизоваться с предоставленными учетными данными'
                )

    return token


if __name__ == '__main__':
    with open('./StepicAPI/config.json', 'r') as file:
        data = json.load(file)

    client_id = data["client_id"]
    client_secret = data["client_secret"]

    try:
        token = get_token(client_id, client_secret)
        print(f'Token: {token}')
    except InvalidToken as e:
        print(e)

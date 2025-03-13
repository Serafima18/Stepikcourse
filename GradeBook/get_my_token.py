import requests

from config import client_id, client_secret

# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)

api_host = 'https://stepik.org'

# client_id = '...'
# client_secret = '...'
# api_host = 'http://127.0.0.1' # save to localhost 

course_id = 401
mode = 'SAVE' # IMPORTANT: use SAVE first, then use PASTE with uncommented (or changed) lines above (client keys and host)

cross_domain = True # to re-upload videos

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post(f'{api_host}/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)

print(f'Token: {token}')
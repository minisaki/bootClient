import requests
import json
from config.base_config import SERVER_DOMAIN


def get_facebook_user(facebook_id):
    request_url = SERVER_DOMAIN+'account/'+facebook_id
    r = requests.get(request_url)
    data = json.loads(r.content)
    return data

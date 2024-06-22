import key_name
import requests
from pprint import pprint


KINOPOISK_URL_FOTO =  '/images'
data_kp = (
    key_name.KINOPOISK_URL + 
    key_name.KINOPOISK_URL_MAIN + 
    str('666') + 
    KINOPOISK_URL_FOTO
)
response_kp = requests.get(data_kp, headers=key_name.DATA_KP)

response_kp = response_kp.json()
pprint(response_kp['items'])

import requests     #요청을 하기 위한 모듈
import pprint
from decouple import config #decouple에서부터 config 호출


base_url = 'https://api.telegram.org'

token = config('API_TOKEN') 

chat_id = config('CHAT_ID')                       #.env파일로 숨긴 후 참조를 활용하여!! 왜냐하면 보안이 중요하니깐

text = "디커플 테스트"

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}' #틀을 만드는 URL
response = requests.get(api_url)
pprint.pprint(response.json()) #이쁘게 표현 해줌
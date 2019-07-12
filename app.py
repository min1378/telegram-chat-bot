from flask import Flask, request
from decouple import config
import pprint
import requests 
app = Flask(__name__)

API_TOKEN = config('API_TOKEN')
#CHAT_ID = config('CHAT_ID')
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')


@app.route('/')
def hello():
    return ''

@app.route('/greeting/<name>')

def greeting(name):
    return f'hello {name}'


@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json()
    #pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None: #딕셔너리 get으로 접근 가능 
        #우리가 원하는 로직
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')
        

        #첫 네글자가 '/번역 ' 일 떄
        if text[0:4] == '/영한 ':  #/한영
            headers = {
                'X-Naver-Client-Id' : NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
            }
            data = {
                'source': 'ko', #'en'
                'target': 'en', #'ko'
                'text' : text[4:] # '/번역 ' 이후의 문자열만 대상으로 번역
            }
            
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')
        #if text == '점심메뉴' :
        #   text = '짜장면이나 먹어!'
        
        #send message
        if text[0:4] == '/한영 ':  #/한영
            headers = {
                'X-Naver-Client-Id' : NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
            }
            data = {
                'source': 'en', #'en'
                'target': 'ko', #'ko'
                'text' : text[4:] # '/번역 ' 이후의 문자열만 대상으로 번역
            }
            
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)
    return '', 200












if __name__ == '__main__' :
    app.run(debug=True)
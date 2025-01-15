#api로 작동 시키고 싶어서 (다른 소프트웨어랑 소통하고 싶어서 다른 서버라고 생각각)
import requests #http 요청 주고 받는 모듈듈

url = "http://127.0.0.1:8000/api/v1/articles/json-drf/" #요청을 보낼 url
response = requests.get(url) #요청을 보내고 데이터를 가지고 옴
print(response) #response.json()하면 json형태의 데이터 출력함

from rest_framework.views import APIView
from rest_framework.response import Response
from .bots import translatebot #여러 챗봇 중에서 번역하는 봇 가지고 옴

class TranslateAPIView(APIView):
    def post(self, request): #body안에 내용 넣을거니까
        user_message = request.data.get("message") #message라는 key로 value값 가지고올거야야
        chatgpt_response = translatebot(user_message) 
        return Response({"message": chatgpt_response})
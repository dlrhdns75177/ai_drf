#데이터를 원하는 형태로 만들기 위해서 (직렬화)

from rest_framework import serializers #rest에서 제공하는 직렬화(유연함)
from .models import Article


class ArticleSerializer(serializers.ModelSerializer): #forms.py랑 같은 형태
    class Meta:
        model = Article
        fields = "__all__"
'''
직렬화 : model에 있는 내용을 가지고 원하는 데이터의형태로 바꾸는 것
그래서 model과 관련이 있는 것이다!
'''
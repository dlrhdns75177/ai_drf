from django.shortcuts import render
from django.http import JsonResponse,HttpResponse #JsonResponse : 장고가 기본적으로 가지고 있는 json 파일로 바꿔주는 것
from django.core import serializers #직접 직렬화하는 코드 작성하지 않아도 자동으로 작성해줌줌
from rest_framework.decorators import api_view
from .models import Article

def article_list_html(request):
    articles = Article.objects.all()
    context = {
        'articles':articles
    }
    return render(request,"articles/article_list.html",context)

def json_01(request):
    articles = Article.objects.all()
    json_articles = []

    for article in articles:
        json_articles.append(
            {
                "title":article.title,
                "content":article.content,
                "created_at":article.created_at,
                "updated_at":article.updated_at,
            }
        )
    return JsonResponse(json_articles, safe=False) 
'''
원래는 html로 render하던 것을 json파일의 형식으로 반환한다는 것
JsonResponse(어떤 데이터를 json으로 보여줄 것인지, 데이터가 json형태라면 safe 작성할 필요 없음)
safe = False : 기본적으로 json은 딕셔너리 형태를 반환하는데 리스트 형식을 반환하기 위해서
'''

def json_02(request):
    articles = Article.objects.all()
    res_data = serializers.serialize("json",articles) #(어떤 형태로 변환?, 어떤 데이터?)
    '''
    장고에서 제공해주는 직렬화는 편하기는 하지만 유연하지는 않다.
    현재 model구조 그대로 보여주기 때문에 client에게 응답을 할 떄 원하는 데이터들만 보여줄 수 있도록 응답할 수 없다.
    그래서 커스텀 할 수 있어야함!!!! -> 그래서 해결하고자 나온 것이 DRF
    '''
    return HttpResponse(res_data,content_type = "application/json")

#DRF 사용하기
def json_drf(request):
    pass
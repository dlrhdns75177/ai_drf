from django.shortcuts import render
from django.http import JsonResponse,HttpResponse #JsonResponse : 장고가 기본적으로 가지고 있는 json 파일로 바꿔주는 것
from django.core import serializers #직접 직렬화하는 코드 작성하지 않아도 자동으로 작성해줌줌
from rest_framework.decorators import api_view #rest에서 제공하는 데코레이터들 중 하나나
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from django.shortcuts import get_object_or_404 #client가 없는 pk에 접근했을 때 404에러 보여줌
from rest_framework import status #다양한 status code 제공 우리가 직접 201 혹은 200 이렇게 적을 필요 없음음

#def article_list_html(request):
#    articles = Article.objects.all()
#    context = {
#        'articles':articles
#    }
#    return render(request,"articles/article_list.html",context)

#def json_01(request):
#    articles = Article.objects.all()
#    json_articles = []

#    for article in articles:
#        json_articles.append(
#            {
#                "title":article.title,
#                "content":article.content,
#                "created_at":article.created_at,
#                "updated_at":article.updated_at,
#            }
#        )
#    return JsonResponse(json_articles, safe=False) 
'''
원래는 html로 render하던 것을 json파일의 형식으로 반환한다는 것
JsonResponse(어떤 데이터를 json으로 보여줄 것인지, 데이터가 json형태라면 safe 작성할 필요 없음)
safe = False : 기본적으로 json은 딕셔너리 형태를 반환하는데 리스트 형식을 반환하기 위해서
'''

#def json_02(request):
#    articles = Article.objects.all()
#    res_data = serializers.serialize("json",articles) #(어떤 형태로 변환?, 어떤 데이터?)
 
'''
    장고에서 제공해주는 직렬화는 편하기는 하지만 유연하지는 않다.
    현재 model구조 그대로 보여주기 때문에 client에게 응답을 할 떄 원하는 데이터들만 보여줄 수 있도록 응답할 수 없다.
    그래서 커스텀 할 수 있어야함!!!! -> 그래서 해결하고자 나온 것이 DRF
    '''
#    return HttpResponse(res_data,content_type = "application/json") #header에 내가 application/json이렇게 형태 바꿨다고 알려주기기

#DRF 사용하기
#@api_view(["GET"]) #client가 get요청을 함
#def json_drf(request):
#    articles = Article.objects.all()
#    serializer = ArticleSerializer(articles, many=True) #단일 객체면 many 작성하지 않아도 됨됨
#    return Response(serializer.data) #json의 형태로 담긴 데이터를 반환하겠다

@api_view(['GET','POST']) #꼭 필요한 부분
def article_list(request):
    if request.method == "GET": #조회만 할거면
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST": #새로운 글 생성 할거면면
        #print(request.data) #터미널에서 print문 확인할 수 있음
        serializer = ArticleSerializer(data=request.data) #새로운 데이터 넣은 객체 생성
        if serializer.is_valid(raise_exception=True): #drf에서 제공하는 직렬화는 장고에서의 modelform과 비슷한 역할할
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #만약에 성공을 했다면 201표시해
        #return Response(serializer.errors, status=400) #raise_exception=True를 하게 되면 is_valid()하지 않을 때 에러발생시킴킴


@api_view(["GET",'PUT', "DELETE"]) 
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)#pk=pk라고 명시해주기
    if request.method == "GET":
        serializer = ArticleSerializer(article) #pk 하나만 가져오니까 many 필요 없음
        return Response(serializer.data)
    
    elif request.method == "PUT": #모두 다 수정하겠다.
        serializer = ArticleSerializer(article, data=request.data, partial =True) #장고의 modelform이랑 형태가 비슷 기존의 데이터에 업데이트를 하는 것
        #partial = True는 부분적으로 수정해도 괜찮다는 것
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_200_OK)
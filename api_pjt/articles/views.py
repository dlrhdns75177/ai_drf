from django.shortcuts import render
from django.http import JsonResponse,HttpResponse #JsonResponse : 장고가 기본적으로 가지고 있는 json 파일로 바꿔주는 것
from django.core import serializers #직접 직렬화하는 코드 작성하지 않아도 자동으로 작성해줌줌
from rest_framework.decorators import api_view #rest에서 제공하는 데코레이터들 중 하나나
from rest_framework.response import Response
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer,CommentSerializer
from django.shortcuts import get_object_or_404 #client가 없는 pk에 접근했을 때 404에러 보여줌
from rest_framework import status #다양한 status code 제공 우리가 직접 201 혹은 200 이렇게 적을 필요 없음음
from rest_framework.views import APIView #클래스 view로 바꾸기 위해서 상속 받아야함(다른 것들도 있음)
from rest_framework.permissions import IsAuthenticated #로그인이 되어 있는 user들만 접근할 수 있도록록

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

#클래스 사용하지 않고 구현
# @api_view(['GET','POST']) #함수형 뷰에서 꼭 필요한 부분
# def article_list(request):
#     if request.method == "GET": #조회만 할거면
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
    
#     elif request.method == "POST": #새로운 글 생성 할거면면
#         #print(request.data) #터미널에서 print문 확인할 수 있음
#         serializer = ArticleSerializer(data=request.data) #새로운 데이터 넣은 객체 생성
#         '''
#         request.data 를 하는 이유는 여러 http요청 방법을 처리하기 위함(post, put, patch)
#         data= 라고 명시를 하는 이유는 명시하지 않으면 instance(기존의 데이터)를 직렬화하게된다.
#         명시해야만 새롭게 post를 통해서 받은 데이터를 직렬화하는 것
#         '''
#         if serializer.is_valid(raise_exception=True): #drf에서 제공하는 직렬화는 장고에서의 modelform과 비슷한 역할할
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED) #만약에 성공을 했다면 201표시해
        #return Response(serializer.errors, status=400) #raise_exception=True를 하게 되면 is_valid()하지 않을 때 에러발생시킴킴


class ArticleListAPIView(APIView): #클래스 형태로 만들고 싶어서

    permission_classes=[IsAuthenticated] #여기 클래스에 해당하는 모든 함수들은 인증이되어 있어야만 사용할 수 있게 됨

    def get(self,request): #각 기능을 함수로 만들었음
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
        
    def post(self,request):
        serializer = ArticleSerializer(data=request.data) #데이터 불러옴(request.data -> 모든 유형의 http 데이터 요청을 처리할 수 있음)
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 



# @api_view(["GET",'PUT', "DELETE"]) 
# def article_detail(request, pk):
#     article = get_object_or_404(Article, pk=pk)#pk=pk라고 명시해주기
#     if request.method == "GET":
#         serializer = ArticleSerializer(article) #pk 하나만 가져오니까 many 필요 없음
#         return Response(serializer.data)
    
#     elif request.method == "PUT": #모두 다 수정하겠다.
#         serializer = ArticleSerializer(article, data=request.data, partial =True) #장고의 modelform이랑 형태가 비슷 기존의 데이터에 업데이트를 하는 것
#         #partial = True는 부분적으로 수정해도 괜찮다는 것
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

#     elif request.method == "DELETE":
#         article.delete()
#         return Response(status=status.HTTP_200_OK)
    

class ArticleDetailAPIView(APIView):
    
    permission_classes=[IsAuthenticated]

    def get_object(self,pk):
        return get_object_or_404(Article, pk=pk)

    def get(self,request,pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article) #pk 하나만 가져오니까 many 필요 없음
        return Response(serializer.data)
    
    def put(self,request,pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial =True) #장고의 modelform이랑 형태가 비슷 기존의 데이터에 업데이트를 하는 것
        #partial = True는 부분적으로 수정해도 괜찮다는 것
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_200_OK)


class ArticleCommentListAPIView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self,reqeust,article_pk):
        article = get_object_or_404(Article,pk=article_pk)
        comments = article.comment.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)
    
    def post(self,request,article_pk):
        article = get_object_or_404(Article,pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            '''
            request 는 body에 있는 내용을 담고 있다!!!

            현재 유효성을 검사할 때 comment필드에는 article이 외래키이기 때문에 필요한데 
            client가 요청본문에 content만 주었고, article은 없으니까 오류 발생(article은 url에 포함되어 있으니까)
            -> 해결하기 위해서 serializers.py에서 read_only_fields로 처리하면 그냥 조회만 하고 지나갈 수 있도록 함
            그럼 유효성 검사 할 때 article이 없어도 다음 코드 실행
            그리고 밑에서 save함(외래키와 함께께)
            '''
            serializer.save(article=article)
            return Response(serializer.data,status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):

    permission_classes=[IsAuthenticated]

    def get_object(self,comment_pk): #중복되는 부분은 하나의 함수로바꿔주기
        return get_object_or_404(Comment,pk=comment_pk)

    def put(self,request,comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


    def delete(self,request,comment_pk):
        comment = self.get_object(comment_pk) #외래키로 이미 연결이 되어 있기 때문에 article 불러올 필요 없음
        comment.delete()
        data = {f"{comment_pk}는삭제됨"}
        return Response(data, status=status.HTTP_204_NO_CONTENT) #값이 아무것도 없어도 되지만 성공 했을 때 어떤 status code를 보여줄 것인가

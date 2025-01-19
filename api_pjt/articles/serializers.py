#데이터를 원하는 형태로 만들기 위해서(직렬화) + 커스텀 
from rest_framework import serializers #rest에서 제공하는 직렬화(유연함)
from .models import Article,Comment


'''
직렬화 : model에 있는 내용을 가지고 원하는 데이터의형태로 바꾸는 것
그래서 model과 관련이 있는 것이다! = modelform이랑 비슷함
'''

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields=("article",)

    def to_representation(self, instance):
        ret = super().to_representation(instance) #원래 CommentSerializer(부모)출력되는 것도 같이 출력하고
        '''
        to_representation 함수는 데이터를 출력하는 과정으로 client가 이해할 수 있는 형태로 데이터를 변환하는 역할
        serializer를 사용하면 내부적으로 to_representaion 함수가 호출되기 때문에 지금까지 json으로 바꿀 수 있었던 것것
        '''
        ret.pop("article")
        return ret #pop으로 제거된 key-value 빼고 나머지가 나온다

    


#serializer로 필드를 추가해도 db테이블에 추가되는 것은 아니다 단순히 json파일로 변환할 때 어떻게 보일 것인가만!
class ArticleSerializer(serializers.ModelSerializer): 
    #forms.py랑 같은 형태(원래 장고에서는 템플릿도 고려해야하니까 모델폼을 사용했지만! 여기에서는 serializers를 사용)
    #comments = CommentSerializer(many=True,read_only=True)
    '''
    comment 테이블에는 article을 외래키로 갖으니까 article에 대한 내용이 있지만
    article 테이블에는 comment 필드가 없다 그런데 article조회만으로 comment를 보고 싶을때
    사실 역참조를 통해서도 확인 할 수 있지만
    더 쉽게 명시적으로 어떤 article에 어떤 comment들이 있는지 확인하고 싶어서
    '''
    #comments_count = serializers.IntegerField(source="comment.count",read_only=True)
    '''
    source를 이용해서 comment테이블에 없는 필드를 추가해서 직렬화할 수 있다
    위에 comments는 그냥 CommentSerializer만든거 가지고 오기만 하면 되니까! 이번에는 CommentSerializer에도 없는 필드 만들고 싶어서
    이 또한 db에 영향은 없지만 comment모델에 없는 필들르 추가할 수 있다는특징이 있다
    source 는 orm으로 접근할 수 있고 .으로 접근가능
    -> 내가 related_name 을 comment로 했기 때문에 comment.count로 접근 기본은 comment_set.count
    '''

    class Meta:
        model = Article
        fields = "__all__"

class ArticleDetailSerializer(ArticleSerializer): #위에 클래스를 상속 받아서 comments 랑 comments_count 필드를 추가하려고
    comments = CommentSerializer(many=True,read_only=True)
    comments_count = serializers.IntegerField(source="comment.count",read_only=True)
    '''
    그냥 Article 모델에 있는 내용만 보여주고 싶을 수도 있고 
    아니면 추가적으로 더 많은 필드를 보여주고 싶을때는
    상속을 받아서 추가적으로 코드 작성하기
    '''
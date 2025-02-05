from django.core.cache import cache #cache 가져오기 (cache에는 key-value 들어감)-> 이전에는 모두 하드디스크에 저장했었음
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

#Look Aside 캐싱 전략
@api_view(['GET'])
def product_list(request):
    cache_key = "product_list" #먼저 서버(django)가 cache에서 데이터 가져오려고 시도해야함
    if not cache.get(cache_key): #그래서 key 만들어주고 그 key값을 가져오도록 함(근데 그 cache에 데이터가 없으면 = cahce miss)
        print("cache miss")
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)
        json_response = serializers.data #현재 json 형태(딕셔너리)로 되어 있으니까
        cache.set(cache_key,json_response,180) #앞에가 key 뒤에 value (이제 cache에 값이 존재) 마지막은 캐시에 몇초동안 데이터 존재할지
    response_date = cache.get(cache_key) #근데 cache에 저장된 데이터가 있으면 get으로 가져오면 됨
    return Response(response_date)



from django.urls import path
from . import views

urlpatterns = [
    #path("html/",views.article_list_html,name="article_list_html"),
    #path("json-01/",views.json_01,name="json_01"),
    #path("json-02/",views.json_02,name="json_02"),
    #path("json-drf/",views.json_drf,name="json_drf"),
    path("",views.article_list,name="articles_list"),
    path("<int:pk>/",views.article_detail,name="article_detail"),
]

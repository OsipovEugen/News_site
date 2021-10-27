
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path, include
from project import settings
from engine.api.api_views import ApiNews, ApiNewsComment


urlpatterns=[
    path('v1/news_list', ApiNews.as_view()),
    path('v1/news_comment/<str:slug>/',ApiNewsComment.as_view()),

]

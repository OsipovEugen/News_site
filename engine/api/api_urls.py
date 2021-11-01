
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path, include
from project import settings
from engine.api.api_views import ApiNews, ApiNewsComment, ApiNewsDetail, ApiCommentsList, ApiRubricsList, ApiRubricsDetail



urlpatterns=[
    path('v1/news_list', ApiNews.as_view()),
    path('v1/news_detail/<str:slug>', ApiNewsDetail.as_view()),

    path('v1/news_comment/<str:slug>',ApiNewsComment.as_view(), name='comments_by_post'),
    path('v1/comments', ApiCommentsList.as_view(), name='all_comments_on_site'),

    path('v1/rubrics', ApiRubricsList.as_view(), name='rubrics_list'),
    path('v1/rubric_detail/<str:slug>', ApiRubricsDetail.as_view(), name='rubric_detail')

]


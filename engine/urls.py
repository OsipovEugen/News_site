from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path, include
from project import settings
from .views import *

urlpatterns = [
	# News model
    path('news/', NewsListView.as_view(), name='news_list_url'),
    path('news/<str:slug>', NewsDetailView.as_view(), name='post_detail_url'),
    path('news/news_create/', NewsCreate.as_view(), name='news_create_url'),
    path('news/<str:slug>/update/', NewsUpdate.as_view(), name='news_update_url'),
    path('news/<str:slug>/delete', NewsDelete.as_view(), name='news_delete_url'),

    # Rubrics model
    path('rubrics_list/', RubricsListView.as_view(), name='rubrics_list_url'),
    path('rubric/<str:slug>', RubricDetailView.as_view(), name='rubric_detail_url'),
    path('rubric/create/', RubricCreate.as_view(), name='rubrics_create_url'),
    path('rubric/update/<str:slug>/', RubricUpdate.as_view(), name='rubric_update_url'),
    path('rubric/<str:slug>/delete', RubricDelete.as_view(), name='rubric_delete_url'),

    # Authors model
    path('authors_list/', AuthorsList.as_view(), name='authors_list_url'),
    path('author/<str:slug>', AuthorDetail.as_view(), name='author_detail_url'),
    path('author/create/', AuthorCreate.as_view(), name='author_create_url'),
    path('author/<str:slug>/delete', AuthorDelete.as_view(), name='author_delete_url'),
    path('author/update/<str:slug>/', AuthorUpdate.as_view(), name='author_update_url'),

    # Auth
    path('login/', LoginView.as_view(), name='login_url'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password_url'),
    path('register/', RegisterView.as_view(), name='register_url'),
    path('logout/', LogOutView.as_view(), name='logout_url'),


    #Profile
    path('profile/', ProfileView.as_view(), name='profile_url'),
    path('profile/edit/<int:pk>', ProfileUpdateView.as_view(), name='profile_edit_url'),
    path('', include('social_django.urls', namespace='social'))


 ]
 
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
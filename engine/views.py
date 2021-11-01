from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
from . import services
from django.views import View

User = get_user_model()

class LikeView(View):
    def fans(self, request, pk=None):
        """Получает всех пользователей, которые лайкнули `obj`.
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = News.likes.all()
        return Response(serializer)



class NewsListView(ListView):
	model = News
	template = 'news_list.html'
	context_object_name = 'posts'
	paginate_by = 1
	def get_context_data(self,  **kwargs):   # добавления контекста в шаблон
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context


class NewsDetailView(DetailView, FormMixin):
	model = News
	template = 'news_detail.html'
	context_object_name = 'news' # Переименование объекта в шаблоне(по дефолту object)
	form_class = CommentForm
	def get_success_url(self, **kawrgs):
		''' Урл для переадресации после заполнения формы'''
		return reverse_lazy('post_detail_url', kwargs={'slug':self.get_object().slug}) # get_object - возвращает объект который данная вьюха обрабатывает, в моем случае определенный пост

	def get_context_data(self, **kwargs):
		""" Фильтрует комментарии, активные или нет """
		context = super().get_context_data()
		context['comments_by_post'] = self.get_object().comments.filter(active=True)
		# context['active_comments'] = Comment.objects.filter(active=True)
		context['model'] = self.get_object()
		context['show'] = True # Отображать Update и Delete в админ панели или нет
		return context

	def post(self, request, *args, **kwargs):
		''' используется для обработки формы, так как в DetailView не предназначена обработка формы, то мы наследуем еще от FormMixin'''	
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else: 
			return self.form_invalid(form)

	def form_valid(self, form):
		''' Проверка валидности формы'''
		self.object = form.save(commit=False) # Берем форму но не сохраняем ее в БД
		self.object.post = self.get_object() # Вытягиваем название поста
		self.object.name = self.request.user # Вытягиваем юзера
		self.object.email = self.request.user.email # Вытягиваем email юзера
		self.object.save() # Сохраняем форму в БД
		return super().form_valid(form)


class NewsCreate(CreateView):
	form_class = NewsForm
	template_name = 'engine/news_create_form.html'
	raise_exception = True



class NewsUpdate(UpdateView):
	model = News
	form_class = NewsForm
	template_name = 'engine/news_update_form.html'
	context_object_name = 'forms'
	raise_exception = True # рейзит 403 ошибку


class NewsDelete(DeleteView):
	model = News
	template_name = 'engine/news_delete_form.html'
	success_url = 'news_list_url'
	raise_exception = True # рейзит 403 ошибку
	def get_success_url(self):
		return reverse('news_list_url')

# RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS # RUBRIC VIEWS 

class RubricsListView(ListView):
	model = Rubrics
	template = 'rubrics_list.html'
	context_object_name = 'rubrics'


class RubricDetailView(DetailView):
	model = Rubrics
	template = 'rubrics_detail.html'
	context_object_name = 'rubrics'

	def get_context_data(self, **kwargs):
		print(self.get_object())
		context = super().get_context_data()
		context['model'] = self.get_object()
		context['show'] = True # Отображать Update и Delete в админ панели или нет
		return context


class RubricCreate(CreateView):
	form_class = RubricForm
	template_name = 'engine/rubric_create_form.html'


class RubricUpdate(UpdateView):
	model = Rubrics
	form_class = RubricForm
	template_name = 'engine/rubric_update_form.html'
	context_object_name = 'forms'
	success_url = reverse_lazy('news_list_url')


class RubricDelete(DeleteView):
	model = Rubrics
	template_name = 'engine/rubric_delete_confirm.html'
	success_url = reverse_lazy('news_list_url')



# AUTHOR VIEWS # AUTHOR VIEWS # AUTHOR VIEWS # AUTHOR VIEWS # AUTHOR VIEWS # AUTHOR VIEWS # AUTHOR VIEWS # AUTHOR VIEWS

class AuthorUpdate(UpdateView):
	model = Authors
	# fields = ['name', 'surname', 'age', 'photo']
	form_class = AuthorForm
	template_name = 'engine/author_update_form.html'
	success_url = reverse_lazy('authors_list_url')

class AuthorsList(ListView):
	model = Authors
	context_object_name = 'authors'
	template_name = 'engine/authors_list.html'



class AuthorDetail(DetailView):
	model = Authors
	context_object_name = 'current_author'
	template_name = 'engine/author_detail.html'

	def get_context_data(self, **kwargs):
		print('222', self.get_object())
		context = super().get_context_data()
		context['model'] = self.get_object()
		context['show'] = True # Отображать Update и Delete в админ панели или нет
		return context
	
	print('111', Authors.objects.get(name='Eugen'))

	
class AuthorDelete(DeleteView):
	model = Authors
	template_name = 'engine/author_delete_confirm.html'
	success_url = reverse_lazy('authors_list_url')


class AuthorCreate(CreateView):
	form_class = AuthorForm
	template_name = 'engine/author_create.html'
	# Так как context_object_name не работает в CreateView я переопределил название контекста таким образом 
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) # получаем словарь context
		context['author_create_form'] = context.pop('form') # заменяем элементы словаря таким образом
		return context



# AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS # AUTH VIEWS 


class LoginView(LoginView):
	""" Вход в учетную запись """
	form_class = LoginForm
	template_name = 'engine/login.html'
	success_url = reverse_lazy('news_list_url')
	def get_success_url(self):
		return self.success_url


class ChangePasswordView(PasswordChangeView):
	"""Смена пароля"""
	form_class = ChangePasswordForm
	template_name = 'engine/change_password.html'
	success_url = reverse_lazy('news_list_url')
	title = ('Password Change')

class RegisterView(CreateView):
	""" Регистрация """
	model = User
	form_class = RegisterForm
	template_name = 'engine/register.html'
	success_url = reverse_lazy('news_list_url')

	def form_valid(self, form):
		""" Реализация втоматического входа после регистрации"""
		form_valid = super().form_valid(form)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password1']
		auth_user = authenticate(username=username, password=password)
		login(self.request, auth_user)
		return form_valid

class LogOutView(LogoutView):
	""" Выход с учетной записи """
	next_page = reverse_lazy('news_list_url')



class ProfileView(ListView):
	model = User
	template_name = 'engine/profile.html'
	context_object_name = 'profile'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['profile'] = User.objects.get(username=self.request.user.username)
		return context


class ProfileUpdateView(UpdateView):
	model = User
	form_class = ProfileUpdateForm
	template_name = 'engine/profile_edit.html'
	context_object_name = 'profile'
	success_url = reverse_lazy('profile_url')














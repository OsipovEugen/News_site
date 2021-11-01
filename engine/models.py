from django.db import models
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.http import HttpResponse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))


class Like(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')


class News(models.Model):
	title = models.CharField(max_length=150, verbose_name='Название новости')
	body = models.TextField(blank=True, verbose_name='Текст новости')
	slug = models.SlugField(unique=True, blank=True)
	pub_time = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(blank=True, verbose_name='Фото')
	rubric = models.ManyToManyField('Rubrics', blank=True, related_name='news')
	authors = models.ManyToManyField('Authors', blank=False, related_name='authors_of_news')
	likes = GenericRelation(Like)


	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('news_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('news_delete_url', kwargs={'slug': self.slug})

	def __str__(self):
		return self.title

	def total_like(self):
		return self.likes.count()
	


	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)


	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'
		ordering = ['-pub_time']


class Rubrics(models.Model):
	title = models.CharField(unique=True, max_length=150, verbose_name='Название рубрики')
	slug = models.SlugField(unique=True, blank=True)


	def get_absolute_url(self):
		return reverse('rubric_detail_url', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('rubric_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('rubric_delete_url', kwargs={'slug':self.slug})

	def __str__(self):
		return self.title


	class Meta:
		ordering = ['title']
		verbose_name = 'Рубрика'
		verbose_name_plural = 'Рубрики'

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)


class Authors(models.Model):
	name = models.CharField(max_length=150, unique=True, verbose_name='Имя')
	surname = models.CharField(max_length=150, unique=True, verbose_name='Фамилия')
	age = models.IntegerField(verbose_name='Возраст')
	email = models.EmailField(max_length=254, verbose_name='E-Mail')
	photo = models.ImageField(upload_to='author_photos', verbose_name='Фото профиля')
	slug = models.SlugField(unique=True, blank=True, allow_unicode=True, editable=False)


	def get_absolute_url(self):
		return reverse('author_detail_url',kwargs={'slug':self.slug})

	def get_update_url(self):
		return reverse('author_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('author_delete_url', kwargs={'slug':self.slug})

	class Meta:
		verbose_name = 'Автор'
		verbose_name_plural = 'Авторы'
		ordering = ['name']

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.name + '-' + self.surname)
		super().save(*args, **kwargs)

	def __str__(self):
		return (self.name + ' ' + self.surname)


class Comment(models.Model):
	name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Имя')
	email = models.EmailField(settings.AUTH_USER_MODEL, blank=True, null=True, )
	body = models.TextField(max_length=300, verbose_name='Комментарий')
	post = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Время написания коммента')
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=False, verbose_name='Прошел модерацию')

	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug':self.slug})


	class Meta:
		verbose_name = 'Коментарий'
		verbose_name_plural = 'Коментарии'
		ordering = ['created']

	def __str__(self):
		return (f'Comment by {self.name} on {self.post}')


class User(AbstractUser):
	COMPANY = 1
	USER = 2
	MALE = 3
	FEMALE = 4

	ROLE_CHOICES = (
		(COMPANY, 'Company'),
		(USER, 'User')
		)
	SEX_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female')
		)

	photo = models.ImageField(upload_to='user_photos', verbose_name='Фото профиля', blank=True, null=True)
	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
	sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES, blank=True, null=True)
	full_name = models.CharField( max_length=100, verbose_name='Имя Фамилия')
	email = models.EmailField(('email address'), blank=False)
	inst_link = models.CharField( max_length=300, blank=True)
	face_link = models.CharField(max_length=300, blank=True)
	lin_ling = models.CharField(max_length=300, blank=True)



# class Follow(models.Model):
# 	follower = models.ForeignKey(User, related_name='who_follows')
# 	followed = models.ForeignKey(User, related_neme='who_is_followed')
# 	follow_time = models.DateTimeField(auto_now=True) 





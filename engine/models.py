from django.db import models
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.http import HttpResponse

def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))



class News(models.Model):
	title = models.CharField(max_length=150, verbose_name='Название новости')
	body = models.TextField(blank=True, verbose_name='Текст новости')
	slug = models.SlugField(unique=True, blank=True)
	pub_time = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(blank=True, verbose_name='Фото')
	rubric = models.ManyToManyField('Rubrics', blank=True, related_name='news')
	authors = models.ManyToManyField('Authors', blank=False, related_name='authors_of_news')


	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('news_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('news_delete_url', kwargs={'slug': self.slug})

	def __str__(self):
		return self.title


	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)


	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'
		ordering = ['-pub_time']


class Rubrics(models.Model):
	title = models.CharField(unique=True, max_length=150,verbose_name='Название рубрики')
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
	photo = models.ImageField(upload_to='profile_photos', verbose_name='Фото профиля')
	slug = models.SlugField(unique=True, blank=True, allow_unicode=True, editable=False)


	def get_absolute_url(self):
		return reverse('author_detail_url',kwargs={'slug':self.slug})

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
	name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Имя')
	email = models.EmailField(User, blank=True, null=True, )
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


# class Vote(models.Model):
# 	UP = 1
# 	DOWN = - 1
# 	VALUE_CHOICES = (  
# 		(UP,'👍' ), # Первый элемент каждого кортежа – это значение, которое будет сохранено в базе данных
# 		(DOWN,'👎') # Второй элемент – название, которое будет отображаться для пользователей
# 		)
# 	value = models.SmallIntegerField(choices=VALUE_CHOICES)
# 	# user = models.ForeignKey()
# 	time_voted = models.DateTimeField(auto_now_add=True)
# 	news = models.ForeignKey('News', on_delete=models.CASCADE)
	
# 	class Meta:
# 		unique_together = ('user', 'movie')



# Create your models here.

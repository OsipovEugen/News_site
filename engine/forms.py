from django import forms
from .models import News, Rubrics, Authors, Comment
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class NewsForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

	class Meta:
		model = News
		fields = ['title', 'body', 'image', 'rubric', 'authors']

	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()

		if new_slug == 'create':
			raise ValidationError('slug may not be "{0}"'.format(self.cleaned_data['slug']))
		return new_slug

	
	def clean(self):
		super().clean()
		errors = {}
		if not self.cleaned_data['body']:
			errors['body'] = ValidationError('Please add news body')
		if errors:
			raise ValidationError(errors)





class RubricForm(forms.ModelForm):

	class Meta:
		model = Rubrics
		fields = ['title']
		widgets = {
		'title': forms.TextInput(attrs={'class':'form-control'}),
		'slug': forms.TextInput(attrs={'class':'form-control'}),
		}

		def clean_title(self):	
			new_title = self.cleaned_data['title'].lower()
			if Rubrics.objects.filter(title__iexact=new_title).count():
				raise ValidationError('WRONG name') # Для создания только уникальных slug
			





class AuthorForm(forms.ModelForm):

	class Meta:
		model = Authors
		fields = ('name', 'surname', 'age', 'email', 'photo')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

	def clean_email(self):
		new_email = self.cleaned_data['email']
		if Authors.objects.filter(email__iexact=new_email).count():
			raise ValidationError('Email has to be unique')
		else:
			return new_email


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('body', )
		widgets = {
		'body':forms.TextInput(attrs={'class':'form-control textarea'}),
		}


class LoginForm(AuthenticationForm,forms.ModelForm):

	class Meta:
		model = User
		fields = ('username', 'password')

	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=254)


	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'email')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	def clean_email(self):
		new_email = self.cleaned_data['email']
		if User.objects.filter(email__iexact=new_email).count():
			raise ValidationError('Email has to be unique')


	



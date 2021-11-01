from django import forms
from .models import News, Rubrics, Authors, Comment, User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, SetPasswordForm


User = get_user_model()

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


class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

	error_messages = {
		**SetPasswordForm.error_messages,
		'password_incorrect':'Your old password is incorrect.Please, try again'
	}

	def clean_old_password(self):
		old_password = self.cleaned_data['old_password']
		if not self.user.check_password(old_password):
			raise ValidationError(
				self.error_messages['password_incorrect']
				)
			return old_password





class RegisterForm(UserCreationForm):


	class Meta:
		model = User
		fields = ('email','username', 'password1', 'password2',  'full_name', 'sex')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

	def save(self, commit=True):
		user = super().save(commit=False)
		print(self.cleaned_data['email'])
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	def clean_email(self):
		new_email = self.cleaned_data['email']
		if User.objects.filter(email__iexact=new_email).count():
			raise ValidationError('Email has to be unique')
		return new_email


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['full_name', 'inst_link', 'face_link' ,'lin_ling']
		labels = {'inst_link':'Instagram', 'face_link':'Facebook'}







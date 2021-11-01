from rest_framework import serializers, permissions, viewsets, generics
from engine.models import News, Authors, Comment, Rubrics
from rest_framework.validators import UniqueValidator


class NewsSerializer(serializers.ModelSerializer):
	authors = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
	rubric = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
	comments = serializers.SlugRelatedField(slug_field='body', many=True, read_only=True)
	class Meta:
		model = News
		fields = ('title', 'body', 'authors', 'rubric', 'comments')

class CommentSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='authors.username')
	# post = serializers.SlugRelatedField(slug_field='title', read_only=True)
	class Meta:
		model = Comment
		fields = ('name', 'email','body', 'post', 'created', 'owner' )


class RubricSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rubrics
		fields = ('title', 'slug')



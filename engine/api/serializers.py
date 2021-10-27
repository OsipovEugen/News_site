from rest_framework import serializers, permissions, viewsets, generics
from engine.models import News, Authors, Comment


class NewsSerializer(serializers.ModelSerializer):
	authors = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
	rubric = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
	class Meta:
		model = News
		fields = ('title', 'body', 'authors', 'rubric') 

class CommentSerializer(serializers.ModelSerializer):
	name = serializers.SlugRelatedField(slug_field='username', read_only=True)
	post = serializers.SlugRelatedField(slug_field='title', read_only=True)
	class Meta:
		model = Comment
		fields = ('name', 'email','body', 'post', 'created' )
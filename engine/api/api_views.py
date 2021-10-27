from django.shortcuts import render	
from rest_framework.views import APIView
from rest_framework import status, generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework import serializers, permissions, viewsets
from engine.models import News, Comment
from .serializers import NewsSerializer, CommentSerializer


class ApiNews(APIView):
	def get(self, request):
		queryset = News.objects.all()
		serializers = NewsSerializer(queryset, many=True)
		return Response(serializers.data)

class ApiNewsComment(APIView):

	def get(self, request, slug):
		news=News.objects.get(slug=slug)
		nc = news.comments.all()
		serializers = CommentSerializer(nc, many=True)
		return Response(serializers.data)

	# def post(self, request, slug):
	# 	news = News.objects.get(slug=slug)
	# 	# news.comments.create(CommentSerializer(data=request.data))
	# 	com = CommentSerializer(data=request.data)
	# 	if com.is_valid(raise_exception=True):
	# 		com.save()
	# 	return Response(serializers.data)


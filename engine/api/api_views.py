from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework import serializers, permissions, viewsets
from engine.models import News, Comment, Rubrics
from .serializers import NewsSerializer, CommentSerializer, RubricSerializer


class ApiNews(APIView):
	def get(self, request):
		queryset = News.objects.all()
		serializer = NewsSerializer(queryset, many=True)
		return Response(serializer.data)

	def post(self, request):
		news = NewsSerializer(data=request.data)
		if news.is_valid(raise_exception=True):
			news.save()
		return Response(status=status.HTTP_201_CREATED, data='Successfully created')


class ApiNewsDetail(APIView):
	def get_object(self, slug):
		return News.objects.get(slug=slug)

	def get(self, request, slug):
		queryset = self.get_object(slug)
		serializer = NewsSerializer(queryset)
		return Response(serializer.data)

	def patch(self, request, slug):
		queryset = self.get_object(slug)
		news_ser = NewsSerializer(queryset, data=request.data)
		if news_ser.is_valid():
			news_ser.save()
			return Response(news_ser.data)
		return Response(status=status.HTTP_400_BAD_REQUEST, data='wrong arguments')

	def delete(self, request, slug):
		queryset = self.get_object(slug)
		queryset.delete()
		return Response(status=status.HTTP_204_NO_CONTENT, data='Succesfully deleted')

class ApiNewsComment(APIView):

	def get(self, request, slug):
		"""Show comments on one news"""
		news = News.objects.get(slug=slug)
		nc = news.comments.all()
		serializers = CommentSerializer(nc, many=True)
		return Response(serializers.data)

	def delete(self,request, slug):
		news = News.objects.get(slug=slug)
		queryset = news.comments.all()
		print(queryset)
		queryset.delete()
		return Response(status=status.HTTP_204_NO_CONTENT, data='Succesfully deleted')


class ApiCommentsList(generics.ListCreateAPIView):
	"""Shows all comments on site and creating comment for news"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save()


class ApiRubricsList(APIView):
	""" Creating and showing a list of rubrics"""
	def get(self, request):
		queryset = Rubrics.objects.all()
		rubric_ser = RubricSerializer(queryset, many=True)
		return Response(rubric_ser.data)

	def post(self, request):
		rubric_ser = RubricSerializer(data=request.data)
		if rubric_ser.is_valid():
			rubric_ser.save()
			return Response(status=status.HTTP_201_CREATED, data='Rubric was successfully created')
		return Response(data=rubric_ser.errors)


class ApiRubricsDetail(APIView):
	"""" Showing detail about rubric, deleting and updating rubric"""
	def get_queryset(self, slug):
		return Rubrics.objects.get(slug=slug)

	def get(self, request, slug):
		queryset = self.get_queryset(slug)
		rubric_ser = RubricSerializer(queryset)
		return Response(rubric_ser.data)

	def put(self, request, slug):
		queryset = self.get_queryset(slug)
		rubric_ser = RubricSerializer(queryset, data=request.data)
		if rubric_ser.is_valid():
			rubric_ser.save()
			return Response(rubric_ser.data)
		return Response(status=status.HTTP_400_BAD_REQUEST, data='Wrong data')

	def delete(self, reques, slug):
		queryset = self.get_queryset(slug)
		queryset.delete()
		return Response(status=status.HTTP_204_NO_CONTENT, data='Successfully deleted')


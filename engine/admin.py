from django.contrib import admin
from .models import *

# admin.site.register(News)

class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_time', 'image')
	list_filter = ('title', 'pub_time', 'rubric')


class RubricsAdmin(admin.ModelAdmin):
	list_display = ('title',)
	list_filter = ('title',)


class AutrhorsAdmin(admin.ModelAdmin):
	list_display = ('name', 'surname', 'photo', 'email')
	list_filter = ('name', 'surname', 'email')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email')
	list_filter = ('name', 'created', 'email', 'active', 'post')
	search_fields = ('name', 'email', 'body')


admin.site.register(News, NewsAdmin)
admin.site.register(Rubrics, RubricsAdmin)
admin.site.register(Authors, AutrhorsAdmin)
admin.site.register(Comment, CommentAdmin)

# Register your models here.

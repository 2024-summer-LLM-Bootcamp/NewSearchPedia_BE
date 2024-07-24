from django.contrib import admin
from .models import Article

# Register your models here.
admin.site.register(Article)

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['article']

admin.site.register(Article, ArticleAdmin)
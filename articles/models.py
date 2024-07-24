from django.db import models
from accounts.models import User
# Create your models here.


class Article(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    news_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    news_list = models.JSONField(blank=True, null=True, default=dict)
    encyc_list = models.JSONField(blank=True, null=True, default=dict)


# class News(models.Model):
#     article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     link = models.URLField()
#     thumbnail = models.TextField()
#     date = models.CharField(max_length=15)


# class Encyc(models.Model):
#     article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
#     keyword = models.CharField(max_length=30)
#     content = models.TextField()
#     encyc_link = models.URLField()

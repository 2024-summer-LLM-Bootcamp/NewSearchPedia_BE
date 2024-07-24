from django.db import models

# Create your models here.

class Article(models.Model):
    article_id = models.IntegerField()
    user_id = models.IntegerField()
    user_input = models.TextField()
    news_summary = models.TextField()
    created_at = models.DateTimeField()


class news(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_Length=100)
    content = models.TextField()
    link = models.URLField()
    thumbnail = models.TextField()
    date = models.DateTimeField()

class encyc(models.Models):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    keyword =  models.CharField(max_length=30)
    content = models.TextField()
    encyc_link = models.URLField()
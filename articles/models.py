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

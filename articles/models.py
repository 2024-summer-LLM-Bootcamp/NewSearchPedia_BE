from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField()
    thumbnail = models.URLField(blank=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 생성 시간 기록
    summary = models.TextField(blank=True, null=True)  # 요약 필드 추가


    def __str__(self):
        return self.title

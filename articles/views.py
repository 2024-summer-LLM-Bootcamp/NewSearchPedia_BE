from django.shortcuts import render, get_object_or_404
from django.http import httpResponse
from .models import Article
from datetime import timezone
import articles

# Create your views here.

def index(request):
    article_list = Article.objects.order.by('-create_date')
    context = {'article_list': article_list}
    # rendering html
    return render(request, 'articles/article_list.html', context)
def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
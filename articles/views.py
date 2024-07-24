from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article
from datetime import timezone
import articles
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    page = request.GET.get('page', '1')
    article_list = Article.objects.order.by('-create_date')
    paginator = Paginator(article_list, 10)
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj}
    # rendering html
    return render(request, 'articles/article_list.html', context)
def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
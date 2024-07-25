from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import Article
from .serializers import ArticleSerializer
from .utils.utils import *

# Create your views here.
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

class Article_View(APIView):
    def get(self, request):
        # TODO: 회원인증 필수
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다!'}, status=status.HTTP_401_UNAUTHORIZED)
        articles = Article.objects.filter(user_id=request.user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        # TODO: 회원인증 필수
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다!'}, status=status.HTTP_401_UNAUTHORIZED)
        print(data)
        query = data['query']

        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)

        new_article = Article(user_id=request.user, user_input=query)

        news_list = get_news(query)
        new_article.news_list = news_list

        summary = generate_summary_from_news_list(news_list)
        new_article.news_summary = summary

        keywords = generate_keyword(summary)
        encyc_list = get_encycs(keywords)
        new_article.encyc_list = encyc_list

        new_article.save()

        serializer = ArticleSerializer(new_article)
        return Response({'messasge': 'created', 'article': serializer.data}, status=status.HTTP_201_CREATED)

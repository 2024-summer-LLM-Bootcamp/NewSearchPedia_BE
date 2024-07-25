from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Article
from .serializers import ArticleSerializer
from .utils.utils import *

# Create your views here.
'''
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
'''


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class Article_View(APIView):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        search = request.GET.get('search')
        if search is None:
            search = ""
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다!'}, status=status.HTTP_401_UNAUTHORIZED)
        articles = Article.objects.filter(
            user_id=request.user, user_input__contains=search)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다!'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
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

        serializer = self.serializer_class(new_article)
        return Response({'messasge': 'created', 'article': serializer.data}, status=status.HTTP_201_CREATED)


class Article_Detail_View(APIView):
    def get(self, request, article_id):
        # auth
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다!'}, status=status.HTTP_401_UNAUTHORIZED)

        article = Article.objects.filter(
            user_id=request.user,
            id=article_id).first()

        # 404 not found
        if article is None:
            return Response({"error": "해당 아티클을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'article': ArticleSerializer(article).data}, status=status.HTTP_200_OK)

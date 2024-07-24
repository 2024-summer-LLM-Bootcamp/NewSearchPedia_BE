from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Article
from .serializers import ArticleSerializer
from .utils.utils import get_news
# Create your views here.


class Article_View(APIView):
    def get(self, request):
        return Response([], status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print(data)
        query = data['query']

        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)

        new_article = Article(user_id=request.user, user_input=query)
        news_list = get_news(query)
        new_article.news_list = news_list

        new_article.save()

        serializer = ArticleSerializer(new_article)
        return Response({'messasge': 'created', 'article': serializer.data}, status=status.HTTP_201_CREATED)

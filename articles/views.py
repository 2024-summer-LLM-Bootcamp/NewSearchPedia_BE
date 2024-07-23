from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import requests
from bs4 import BeautifulSoup
from .models import News
from dotenv import load_dotenv
from dateutil import parser
from pydantic import BaseModel, Field
from typing import List
import time

# 환경 변수 로드
load_dotenv()

# 네이버 뉴스 API 키 설정
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# Azure OpenAI API 키와 엔드포인트 URL 설정
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("OPENAI_API_VERSION")

# 요청 헤더 설정
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# NewsSerializer 정의
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

# NewsViewSet 정의
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

# 뉴스 본문 및 썸네일 가져오기 함수
def get_news_content_and_thumbnail(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        if 'news.naver.com' in url:
            content = soup.select_one('#dic_area')
            thumbnail = soup.select_one('meta[property="og:image"]')
            content_text = content.get_text(strip=True) if content else "본문을 가져올 수 없습니다."
            thumbnail_url = thumbnail['content'] if thumbnail else ""
            return content_text, thumbnail_url
        article = soup.find('article')
        content_text = article.get_text(strip=True) if article else "본문을 가져올 수 없습니다."
        thumbnail = soup.select_one('meta[property="og:image"]')
        thumbnail_url = thumbnail['content'] if thumbnail else ""
        return content_text, thumbnail_url
    except Exception as e:
        return "본문을 가져올 수 없습니다.", ""

# Azure OpenAI 요청 함수
def get_keywords_from_query(query):
    data = {
        "temperature": 0.3,
        "max_tokens": 50,
        "messages": [
            {"role": "system", "content": "You are an assistant that extracts relevant keywords from user queries."},
            {"role": "user", "content": f"Extract the most relevant keywords from the following query: '{query}'"}
        ]
    }
    url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    response = requests.post(url, headers=headers, json=data)
    keywords = response.json()["choices"][0]["message"]["content"]
    return keywords.strip()

# 네이버 뉴스 API 호출 함수
def get_news_from_naver(query, display, start):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}&start={start}"
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 뉴스 데이터를 받아와서 처리하는 함수
def fetch_and_process_news(query):
    news_data = get_news_from_naver(query, 100, 1)
    news_list = []
    if news_data and 'items' in news_data:
        articles_content = []
        for item in news_data['items']:
            if len(news_list) < 10:
                title = item['title']
                link = item['link']
                pubDate = parser.parse(item['pubDate'])
                content, thumbnail = get_news_content_and_thumbnail(link)
                news = News(
                    title=title,
                    content=content,
                    link=link,
                    thumbnail=thumbnail,
                    date=pubDate
                )
                news_list.append(news)
                articles_content.append(content)
                time.sleep(0.5)
            if len(news_list) == 10:
                break
        summary = summarize_articles(articles_content).summary
        for news in news_list:
            news.summary = summary
        News.objects.bulk_create(news_list)
    return news_list

# Pydantic 모델 정의
class ArticleSummary(BaseModel):
    summary: str = Field(..., title="Summary of the combined news articles")

# 뉴스 기사 요약 함수 정의
def summarize_articles(articles_content: List[str]) -> ArticleSummary:
    combined_content = "\n\n".join(articles_content)
    data = {
        "temperature": 0.5,
        "max_tokens": 300,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant specialized in summarizing news articles. Please provide a concise summary of the following combined news articles in Korean, including only the most important and relevant points in a single paragraph."},
            {"role": "user", "content": combined_content}
        ]
    }
    url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    response = requests.post(url, headers=headers, json=data)
    summary_text = response.json()["choices"][0]["message"]["content"]
    return ArticleSummary(summary=summary_text)

@api_view(['GET'])
def summarize_news(request):
    query = request.GET.get('query', None)
    if not query:
        return Response({"error": "Query parameter is required"}, status=400)
    keywords = get_keywords_from_query(query)
    news_list = fetch_and_process_news(keywords)
    articles_content = [news.content for news in news_list]
    summary = summarize_articles(articles_content)
    return Response({"summary": summary.summary})

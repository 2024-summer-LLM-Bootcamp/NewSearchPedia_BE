import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
import json

# 환경 변수 로드
load_dotenv()

# 네이버 뉴스 API 키 설정
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

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

# 뉴스 본문 가져오기 함수
def get_news_content(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 네이버 뉴스인 경우
        if 'news.naver.com' in url:
            content = soup.select_one('#dic_area')
            if content:
                return content.get_text(strip=True)
        
        # article 태그 찾기
        article = soup.find('article')
        if article:
            return article.get_text(strip=True)
        
        # article 태그가 없으면 body 내용 가져오기
        body = soup.find('body')
        if body:
            return body.get_text(strip=True)
        
        return "본문을 가져올 수 없습니다."
    except:
        return "본문을 가져올 수 없습니다."

# 뉴스 클래스 정의
class News(BaseModel):
    title: str
    content: str
    link: str
    thumbnail: str
    date: str

# 검색어 입력
query = input("검색할 키워드를 입력해주세요: ")

# 결과 저장 리스트
news_list = []

# 뉴스 데이터를 받아와서 처리하는 함수
def fetch_and_process_news(query):
    news_data = get_news_from_naver(query, 100, 1)
    if (news_data and 'items' in news_data):
        for item in news_data['items']:
            if len(news_list) < 10:
                title = item['title']
                link = item['link']
                pubDate = item['pubDate']
                thumbnail = item.get('thumbnail', '')

                # 본문 내용 가져오기
                content = get_news_content(link)

                # 뉴스 객체 생성
                news = News(
                    title=title,
                    content=content,
                    link=link,
                    thumbnail=thumbnail,
                    date=pubDate
                )

                news_list.append(news)

                # 과도한 요청을 방지하기 위해 잠시 대기
                time.sleep(0.5)

            if len(news_list) == 10:
                break

# 뉴스 크롤링 시작
fetch_and_process_news(query)

# 결과 출력
for i, news in enumerate(news_list):
    print(f"[뉴스 {i + 1}]")
    print(f"제목: {news.title}")
    print(f"링크: {news.link}")
    print(f"썸네일: {news.thumbnail}")
    print(f"날짜: {news.date}")
    print(f"내용: {news.content}\n")  # 전체 내용 출력

# 데이터 프레임으로 만들기
news_df = pd.DataFrame([news.dict() for news in news_list])

# 데이터 프레임 저장
now = datetime.datetime.now()
news_df.to_csv(f'{query}_{now.strftime("%Y%m%d_%H%M%S")}.csv', encoding='utf-8-sig', index=False)

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

    # 엔드포인트 URL 구성
    url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"

    # POST 요청 보내기
    response = requests.post(url, headers=headers, json=data)

    # 응답 출력
    summary_text = response.json()["choices"][0]["message"]["content"]
    
    # Pydantic 모델 인스턴스로 변환
    summary = ArticleSummary(summary=summary_text)
    return summary

# 뉴스 기사 요약
summary = summarize_articles([news.content for news in news_list])
print("\n요약:\n", json.dumps(summary.model_dump(), indent=2, ensure_ascii=False))

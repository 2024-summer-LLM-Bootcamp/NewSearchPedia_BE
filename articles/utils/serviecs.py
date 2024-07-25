import os
import dotenv

import requests
from bs4 import BeautifulSoup

from rest_framework.exceptions import APIException

# 환경 변수 로드
dotenv.read_dotenv()


# 네이버 뉴스 API 키 설정
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

naver_req_headers = {
    'X-Naver-Client-Id': client_id,
    'X-Naver-Client-Secret': client_secret
}


def naver_api_service(url):
    response = requests.get(url, headers=naver_req_headers)
    print("--naver_api_service--\n", response.json())

    if response.status_code == 200:
        return response.json()
    else:
        raise APIException("naver 검색 api 요청에 실패했습니다.", 500)


def get_news_content_and_thumbnail(url):
  # 뉴스 본문 및 썸네일 가져오기 함수
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        # if 'news.naver.com' in url:
        #     content = soup.select_one('#dic_area')
        #     content_text = content.get_text(
        #         strip=True) if content else "본문을 가져올 수 없습니다."
        #     thumbnail = soup.select_one('meta[property="og:image"]')
        #     thumbnail_url = thumbnail['content'] if thumbnail else ""
        #     return content_text, thumbnail_url
        article = soup.find('article')
        content_text = article.get_text(
            strip=True) if article else "본문을 가져올 수 없습니다."
        thumbnail = soup.select_one('meta[property="og:image"]')
        thumbnail_url = thumbnail['content'] if thumbnail else ""
        return content_text, thumbnail_url
    except Exception as e:
        raise APIException("뉴스 content 크롤링에 실패했습니다.", 500)


# Azure OpenAI API 키와 엔드포인트 URL 설정
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("OPENAI_API_VERSION")

# 요청 헤더 설정
openai_req_headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}


def openai_api(data):
    url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    response = requests.post(url, headers=openai_req_headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

import os
import dotenv

from .serviecs import naver_api_service


# 환경 변수 로드
dotenv.read_dotenv()


# Azure OpenAI API 키와 엔드포인트 URL 설정
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("OPENAI_API_VERSION")


def get_news(query):
    '''
    naver API 기사 리스트 반환
    '''
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&start=1"

    news_list = naver_api_service(url)['items']

    ''' ouput 예시
    [{
        "title": "일론 머스크, <b>트럼프</b>의 전기차 지원 철회는 경쟁업체에 치명적",
        "originallink": "https://www.tokenpost.kr/article-188540",
        "link": "https://www.tokenpost.kr/article-188540",
        "description": "머스크는 이달 초 <b>트럼프</b> 후보에 대한 <b>암살</b> 시도 직후 <b>트럼프</b>에 대한 지지를 발표했다. 머스크는 자신이 <b>트럼프</b>에게 월 4,500만 달러를 기부하겠다고 약속했다는 언론 보도를 부인했지만, 정치 행동 위원회를 만들었다고... ",
        "pubDate": "Wed, 24 Jul 2024 15:22:00 +0900"
    },]
    '''
    # title
    # content
    # link
    # thumbnail
    # date
    return news_list


def crawling_news():
    '''
    기사 리스트 내용 크롤링 후 기사 객체 생성 및 리스트 반환
    '''
    return []


def generate_summary_text():
    '''
    크롤링한 기사 내용으로 요약문 생성
    '''
    return ""


def generate_keyword():
    '''
    요약문에서 키워드 추출
    '''
    return ""


# 네이버 백과사전 API -> return 백과사전 리스트
def naver_encyc_api():
    '''
    백과사전 객체 생성 및 리스트 반환
    '''
    return []

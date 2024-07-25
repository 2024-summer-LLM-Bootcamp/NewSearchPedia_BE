import os
from pydantic import BaseModel
from .serviecs import naver_api_service, get_news_content_and_thumbnail, openai_api

# 뉴스 클래스 정의


class News(BaseModel):
    title: str
    content: str
    link: str
    thumbnail: str
    date: str


class Encyc(BaseModel):
    title: str
    link: str
    thumbnail: str


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
    return crawling_news(news_list)


def crawling_news(item_list):
    '''
    기사 리스트 내용 크롤링 후 기사 객체 생성 및 리스트 반환
    '''
    news_list = []
    for item in item_list:
        title = item['title']
        link = item['link']
        pubDate = item['pubDate']
        # 본문 내용 및 썸네일 가져오기
        content, thumbnail = get_news_content_and_thumbnail(link)

        # 뉴스 객체 생성
        news = News(
            title=title,
            content=content,
            link=link,
            thumbnail=thumbnail,
            date=pubDate
        )

        news_list.append(news.dict())
    return news_list


def generate_summary_from_news_list(news_list: News):
    '''
    크롤링한 기사 내용으로 요약문 생성
    '''
    contents = [news['content'] for news in news_list]
    combined_content = "\n\n".join(contents)

    data = {
        "temperature": 0.5,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant specialized in summarizing news articles. Please provide a concise summary of the following combined news articles in Korean, including only the most important and relevant points in a single paragraph. 자주 나오는 내용이나 중요한 정보를 요약해줘"},
            {"role": "user", "content": combined_content}
        ]}

    summary = openai_api(data)

    return summary


def generate_keyword(summary):
    '''
    요약문에서 키워드 추출
    '''

    # system_prompt_str = """
    # You are an assistant for identifying and extracting key phrases or keywords from a given context that are useful for further searches in an encyclopedia or database. Ensure the keywords are specific and provide sufficient context for comprehensive searches.
    # Extract specific and contextually rich keywords from the given news article that are useful for encyclopedia search. Each keyword must contain the source of the keyword.
    # For example, instead of 'medical issue', use 'Joe Biden's medical issue'. Instead of "inflation", use 'inflation of US'. Use the following pieces of retrieved context to answer the question. Instead of "a peaceful solution", use "a peaceful solution to the war in Ukraine". Instead of "Conditions for the end of the war", use " in Ukraine". Use "conditions for establishing an allegation of breach of duty" instead of "alleged breach of duty". Don't put simple facts like "67 polls Trump 47.4% Harris 45.4%" as keywords.
    # {summary} """.strip()

    system_prompt_str = f"Extract key phrases or keywords from the given news article that are useful for encyclopedia searches. Provide contextually rich and specific keywords {summary}"

    data = {
        "temperature": 0.3,
        "max_tokens": 50,
        "messages": [
            {"role": "system", "content": system_prompt_str},
            {"role": "user", "content": ""}
        ]
    }

    keywords = openai_api(data)
    return keywords.strip()


# 네이버 백과사전 API -> return 백과사전 리스트
def get_encycs(query):
    '''
    백과사전 객체 생성 및 리스트 반환
    '''
    encyc_list = []

    url = f"https://openapi.naver.com/v1/search/encyc.json?query={query}&display=10&start=1"

    item_list = naver_api_service(url)['items']

    for item in item_list:
        encyc_list.append(Encyc(
            title=item['title'], link=item['link'], thumbnail=item['thumbnail']).dict())

    return encyc_list

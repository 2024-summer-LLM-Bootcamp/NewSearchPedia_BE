import os
import dotenv

import requests

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

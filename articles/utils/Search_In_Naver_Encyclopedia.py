# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
client_id = ""
client_secret = ""
# encText = urllib.parse.quote("검색할 단어")
encText = urllib.parse.quote("")

url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if (rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

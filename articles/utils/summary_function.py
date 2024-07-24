# 요약 함수
def summarize_text(text):
    client = AzureOpenAI(
        api_key=str_api_key,  # Azure Open AI Key
        api_version=str_api_version,  # Azue OpenAI API model
        azure_endpoint=str_endpoint  # Azure Open AI end point(매직에꼴)
    )
    template = """
당신은 텍스트 요점 정리 함수이며, 반환값은 반드시 JSON 데이터여야 합니다.
STEP별로 작업을 수행하면서 그 결과를 아래의 출력 결과 JSON 포맷에 작성하세요.
STEP-1. 아래 세 개의 백틱으로 구분된 텍스트를 원문 그대로 읽어올 것
STEP-2. 텍스트를 요약하세요. 

...

다음의 말투로 번역할 것:["지구의 나이는 45억 살이다.", "세종대왕은 조선의 위대한 국왕이다."]
```{text}```
---
출력 결과: {{"STEP-1": text의 첫 50글자,  "STEP-2": <text를 요약한 결과>}} 
"""

    template = template.format(text=text)

    context = [{"role": "user", "content": template}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=context,
        temperature=0,
        top_p=0,
        seed=1234
    )
    summary = response.choices[0].message.content
    print(summary)
    # llm = OpenAI(api_key=openai.api_key)
    # prompt = PromptTemplate(
    #     input_variables=["text"],
    #     template="Please summarize the following meeting transcript:\n\n{text}"
    # )
    # chain = LLMChain(llm=llm, prompt=prompt)
    # summary = chain.run(text=text)
    return summary

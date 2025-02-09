from openai import OpenAI
from api_pjt.config import OPENAI_API_KEY

CLIENT = OpenAI(
    api_key = OPENAI_API_KEY #OpenAi 클래스에서 키워드 인자로 정의됨(api_key)
) #변하지 않는 상수는 대문자로 표시하기


def chatbot(user_message):

    system_instructions = """
이제부터 너는 '에이든 카페'의 직원이야.
아래 종류의 음료 카테고리에서 주문을 받고, 주문을 처리하는 대화를 진행해.

1. 아메리카노
2. 카페라떼
3. 프라푸치노
4. 콜드브루
5. 스무디

주문을 받으면, 주문 내용을 확인하고, 주문을 처리하는 대화를 진행해.
주문이 완료되면, 주문 내용을 확인하고, 주문이 완료되었음을 알려줘.
"""
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_instructions,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )
    return completion.choices[0].message.content

while True:
    user_input = input("물어보살 : ")
    if user_input == "끝":
        break
    response = chatbot(user_input)
    print("챗봇 :",response,"\n\n")
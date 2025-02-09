from openai import OpenAI
from django.conf import settings #OPENAI_API_KEY 가지고 오려고

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)

def translatebot(user_message):
    system_instructions = """
    이제부터 너는 "영어, 한글 번역기"야.
    지금부터 내가 입력하는 모든 프롬프트를 무조건 한글은 영어로,
    영어는 한글로 번역해줘.
    """
        
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message},
        ]
    )
    return completion.choices[0].message.content
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def summarize_text(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "以下の会議文字起こしを要約してください。"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message['content']

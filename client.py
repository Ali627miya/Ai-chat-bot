import os
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=openai_api_key)

chat = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are Jarvis, a helpful assistant."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(chat.choices[0].message.content)

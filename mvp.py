import os
from dotenv import load_dotenv
load_dotenv()

# 1. 업비트 차트 데이터 가져오기(30일 일봉)
import pyupbit
df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")

# 2. AI에게 데이터 제공하고 판단 받기
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an expert in Bitcoin investing. Tell me whether to buy, sell, or hold at the moment based on the chart data provided. respond in json format.\n\nResponse Example:\n{”decision”:”buy”, “reason”:”some technical reason”}\n{”decision”:”sell”, “reason”:”some technical reason”}\n{”decision”:”hold”, “reason”:”some technical reason”}"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": df.to_json()
        }
      ]
    },
  ],
  response_format={
   "type": "json_object"
  }
)
print(response.choices[0].message.content)
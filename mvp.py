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
result = response.choices[0].message.content

# 3. AI의 판단에 따라 실제로 자동매매 진행하기
import json
result = json.loads(result)
import pyupbit
access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")
upbit = pyupbit.Upbit(access, secret)

if result["decision"] == "buy":
    print(upbit.buy_market_order("KRW-BTC", upbit.get_balance("KRW")))
    print(result["reason"])
elif result["decision"] == "sell":
    print(upbit.sell_market_order("KRW-BTC", upbit.get_balance("KRW-BTC")))
    print(result["reason"])
elif result["decision"] == "hold":
    print(result["reason"])
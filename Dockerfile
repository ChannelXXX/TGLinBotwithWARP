# အဆင့် (၁) - API Server Binary ကို ယူမယ်
FROM aiogram/telegram-bot-api:latest AS api-helper

# အဆင့် (၂) - Python ပတ်ဝန်းကျင်ဆောက်မယ်
FROM python:3.9-slim

# Binary ကို ကူးထည့်မယ်
COPY --from=api-helper /usr/local/bin/telegram-bot-api /usr/bin/telegram-bot-api

# လိုအပ်သော Library များသွင်းမယ်
RUN apt-get update && apt-get install -y libssl-dev procps ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Render က ပေးတဲ့ Port ကို သုံးပြီး Bot ရော API Server ပါ run မယ်
CMD ["sh", "-c", "/usr/bin/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH & python main.py"]

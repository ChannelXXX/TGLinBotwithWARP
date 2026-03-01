FROM aiogram/telegram-bot-api:latest AS api-helper
FROM python:3.9-slim

# Binary ကူးယူခြင်း
COPY --from=api-helper /usr/local/bin/telegram-bot-api /usr/bin/telegram-bot-api

RUN apt-get update && apt-get install -y libssl-dev procps ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Render က Port 8080 ကို စစ်ဆေးမှာဖြစ်လို့ အဲဒီ Port ကို ဖွင့်ပေးထားရပါမယ်
EXPOSE 8080

# API Server ရော Bot ပါ Run မယ်
CMD ["sh", "-c", "/usr/bin/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH & python main.py"]

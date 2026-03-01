FROM node:18-slim

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Render အတွက် Port ဖွင့်ပေးခြင်း (Optional but recommended)
EXPOSE 8080

CMD ["node", "index.js"]

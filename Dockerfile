FROM python:3.9-slim

WORKDIR /lokatir_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/bot/bot.py"]

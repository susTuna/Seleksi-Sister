FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget && \
    wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "wait-for-it.sh db:5432 -t 60 && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
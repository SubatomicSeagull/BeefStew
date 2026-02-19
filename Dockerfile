FROM python:3.13-slim

RUN apt-get update -y && apt-get install -y git libpq-dev gcc ffmpeg libopus-dev espeak-ng curl unzip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deno.land/install.sh | sh

WORKDIR /BeefStew

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]

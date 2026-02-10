FROM python:3.13-slim

RUN apt-get update -y && apt-get install -y git libpq-dev gcc ffmpeg libopus-dev espeak-ng && rm -rf /var/lib/apt/lists/*

WORKDIR /BeefStew

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]

FROM python:3.10-slim

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install git -y
RUN apt-get install libpq-dev gcc -y

RUN git clone https://github.com/SubatomicSeagull/BeefStew.git

WORKDIR /BeefStew

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]
FROM python:3.8.3-slim-buster

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

COPY ./entrypoint.sh .
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
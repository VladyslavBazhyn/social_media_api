FROM python:3.11-alpine
LABEL authors="mr.darmstadtium@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8765"]

 FROM python:3.6-stretch
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
 WORKDIR /code/axbot
 EXPOSE 8000

FROM python:3.6-stretch
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt \
	&& find /root/.cache -name pip -type d -prune -exec rm -r {} \;

COPY . /code/
WORKDIR /code/axbot
EXPOSE 8000

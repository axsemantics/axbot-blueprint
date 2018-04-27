FROM python:3.6-alpine3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN apk update \
	&& apk add --no-cache \
		postgresql-libs \
	&& apk add --no-cache --virtual .build-deps \
		gcc \
		musl-dev \
		postgresql-dev \
	&& python3 -m pip install -r requirements.txt --no-cache-dir \
	&& apk --purge del .build-deps \
	&& find /root/.cache -name pip -type d -prune -exec rm -r {} \;

COPY . /code/
WORKDIR /code/axbot
EXPOSE 8000

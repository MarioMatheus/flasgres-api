FROM python:3.9-alpine

EXPOSE 5000

RUN apk update && apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            musl-dev \
            postgresql-dev \
            build-base \
            linux-headers \
            pcre-dev
RUN apk add --no-cache pcre bash gcc postgresql-libs libc-dev

WORKDIR /app
COPY . /app
COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt
RUN apk del .build-dependencies && rm -rf /var/cache/apk/*
RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

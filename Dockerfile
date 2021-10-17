FROM python:3.8-alpine
LABEL maintainer="horryruo"
WORKDIR /bot
COPY ./requirements.txt .
COPY ./start.sh .
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    apk update && apk add --no-cache \
    chromium \
    chromium-chromedriver \
    libexif \
    udev \
    git &&\
    apk add --no-cache --virtual .build-dependencies \
    tzdata \
    libffi-dev \
    libxslt-dev \
    libxml2-dev \
    gcc \
    musl-dev &&\
    pip install --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt && \
    if [[ ! -f /usr/bin/python ]]; then ln -s /usr/bin/python3 /usr/bin/python; fi && \
    ln -s /bin/bash /usr/bin/bash && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo "Asia/Shanghai" > /etc/timezone &&\
    apk del .build-dependencies && \
    rm -Rf /var/cache/* && \
    chmod 777 /bot/start.sh
ENTRYPOINT [ "sh", "start.sh" ]
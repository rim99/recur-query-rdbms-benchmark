FROM python:3.9.7-alpine3.14

WORKDIR /usr/src/app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
    apk update && \
    apk upgrade && \
    apk add postgresql-dev gcc musl-dev mariadb-dev
RUN pip install mysql-connector-python psycopg2-binary mariadb

CMD [ "python", "app.py" ]
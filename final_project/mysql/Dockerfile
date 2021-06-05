FROM mysql:latest

WORKDIR .

ADD . /mysql_db

COPY init.sql /docker-entrypoint-initdb.d/

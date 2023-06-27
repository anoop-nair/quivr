FROM postgres:15.3

MAINTAINER Anoop Nair

RUN apt-get update && apt-get install -y postgresql-contrib && apt-get install -y postgresql-15-pgvector

ADD createExtensions.sh /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/createExtensions.sh
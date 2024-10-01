ARG PSQL_VERSION=17
FROM postgres:${PSQL_VERSION}
ARG PSQL_VERSION=17

RUN apt-get update &&\
    apt-get install -y postgresql-server-dev-${PSQL_VERSION} tar gzip make gcc python3 python3-psycopg2 python3-pandas python3-sqlalchemy

ADD https://github.com/postgrespro/pgsphere/archive/master.tar.gz pgsphere-master.tar.gz
RUN tar -zxf pgsphere-master.tar.gz && \
	cd pgsphere-master && \
	make USE_HEALPIX=0 USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config && \
	make USE_HEALPIX=0 USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config install && \
	cd .. && \
	rm -rf pgsphere-master pgsphere-master.tar.gz

COPY docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/
COPY fill_tables.py /fill_tables.py

ENV POSTGRES_HOST_AUTH_METHOD trust
ENV PYTHONUNBUFFERED 0

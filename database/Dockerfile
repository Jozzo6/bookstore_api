FROM postgres:latest

COPY *.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_DB=bookstore
ENV POSTGRES_USER=dev
ENV POSTGRES_PASSWORD=testing

EXPOSE 5432
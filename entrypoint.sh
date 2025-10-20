#!/bin/bash
MANAGEPY=src/manage.py

while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do echo "En attente du demarrage de postgresql" && sleep 1; done
if ! PGPASSWORD=8Fny?aXEFkh9ePA3 psql -U postgres -h $POSTGRES_HOST -p $POSTGRES_PORT -lqt | cut -d \| -f 1 | cut -d ' ' -f 2 | grep -q "^bank_db$"; then
    PGPASSWORD=8Fny?aXEFkh9ePA3 createdb -U postgres -h $POSTGRES_HOST -p $POSTGRES_PORT bank_db
else
    echo "La database existe deja"
fi

${MANAGEPY} makemigrations && ${MANAGEPY} migrate
cd src && gunicorn exalt_hexarch.wsgi:application --bind 0.0.0.0:8000

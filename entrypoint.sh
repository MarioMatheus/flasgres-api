#!/usr/bin/env bash
while !</dev/tcp/db/5432; do sleep 5; done; flask db upgrade && uwsgi --ini ./wsgi.ini

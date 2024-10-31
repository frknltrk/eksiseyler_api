#!/bin/sh
crontab /code/etl/crontab && fastapi run /code/app/main.py

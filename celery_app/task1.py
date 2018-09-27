# encoding: utf-8
from celery_app import app
import time

@app.task
def add(x, y):
    time.sleep(2)
    return x+y


@app.task
def multiply(x, y):
    time.sleep(2)
    return x*y



# -*- coding:UTF-8 -*-
import celery


@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y

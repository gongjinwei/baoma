# -*- coding:UTF-8 -*-
import celery
from .SmsClient import countdown_send
from .models import Order
from datetime import datetime


@celery.task
def add(x, y):
    return x + y


@celery.task
def countdown_task(template_id='smsTpl:b339cd8b-9c09-4669-bf34-315c7d2b3106',**kwargs):
    order_id = kwargs.pop('order_id',0)
    print('order_id:%s'%order_id)
    is_exist = Order.objects.filter(order_id=int(order_id)).exists()
    if is_exist:
        order_instance = Order.objects.get(pk=int(order_id))
        expire_time = datetime.fromtimestamp(order_instance.createtime + 3600)
        now = datetime.now()
        if order_instance.order_state != 10 and now > expire_time:
            name = kwargs.pop('name')
            phone_number = kwargs.pop('phone_number')
            print('name:%s,phone:%s'%(name,phone_number))
            time_str = datetime.strftime(expire_time, '%Y-%m-%d %H:%M')
            content_var_dict = {'name': name, 'time': time_str}
            return countdown_send(template_id, phone_number, content_var_dict)
        else:
            print('无需发送')
            return '无需发送'
    else:
        print('订单号不存在')
        return '订单号不存在'

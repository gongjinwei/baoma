# -*- coding:UTF-8 -*-
from django.core.cache import cache
from random import Random
import logging

from baidubce.services.sms.sms_client import SmsClient
from baidubce.exception import BceServerError
from baidubce.exception import BceHttpClientError

from baoma import sms_client_conf as conf


class SmsSender(object):
    sms_client = SmsClient(conf.config)
    random_length = 6
    random_chars = '1234567890'
    invoke_id = conf.invoke_id
    template_id = conf.template_id

    def __init__(self, receiver, random_length=None, random_chars=None):
        self.receiver = receiver
        if random_length:
            self.random_length = random_length
        if random_chars:
            self.random_chars = random_chars

    @property
    def logger(self):
        logger = logging.getLogger('baidubce.services.sms.smsclient')
        fh = logging.FileHandler('sms_error.log')

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        return logger

    def random_str(self):
        strs = ''
        chars = self.random_chars
        length = len(chars) - 1
        random = Random()
        for i in range(self.random_length):
            strs += chars[random.randint(0, length)]
        return strs

    def send(self, type='register'):
        if not isinstance(type,str):
            return (400,'发送类型错误')
        try:
            ttl = cache.ttl(self.receiver + type + '_timeout')
            if ttl > 0:
                return (400,'请在一分钟后再试')
            deliver_str = self.random_str()
            content_var = {'code': deliver_str}
            response = self.sms_client.send_message_2(self.invoke_id, self.template_id, self.receiver, content_var)
            cache.set(self.receiver + type +'_timeout', 60, 60)
            cache.set(deliver_str + type+'_mobile', self.receiver, 900)

            return (int(response.code),'发送成功')

        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                self.logger.error('send message failed. Response %s, _msg: %s'
                                  % (e.last_error.status_code, e.last_error.message))
            else:
                self.logger.error('send message failed. Unknown exception: %s' % e)
            return (int(e.last_error.code),'系统繁忙')

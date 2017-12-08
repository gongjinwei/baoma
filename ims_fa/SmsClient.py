# -*- coding:UTF-8 -*-
import logging

from baidubce.services.sms.sms_client import SmsClient
from baidubce.exception import BceServerError
from baidubce.exception import BceHttpClientError

import sms_client_conf

logger = logging.getLogger('baidubce.services.sms.smsclient')
fh = logging.FileHandler('sms_sample.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
CONF = sms_client_conf

sms_client = SmsClient(CONF.config)

try:
    invoke_id ='OCWGzUKl-y5gn-VgG3'
    template_id ='smsTpl:a054f946-87d6-4a10-ba7f-8953d17b961f'
    receiver ='13868960769'
    content_var ={'code':'111112'}
    response = sms_client.send_message_2(invoke_id,template_id,receiver,content_var)
    print(response.request_id)

except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        logger.error('send message failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        logger.error('send message failed. Unknown exception: %s' % e)



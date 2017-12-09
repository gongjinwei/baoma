# -*- coding:UTF-8 -*-
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.protocol import HTTP

host = 'sms.bj.baidubce.com'
access_key_id = '331691219c464317ac1567d516ec6075'
secret_access_key = b'1f5c53505515416d91cdc275541d7403'
invoke_id = 'OCWGzUKl-y5gn-VgG3'
template_id = 'smsTpl:a054f946-87d6-4a10-ba7f-8953d17b961f'

config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), protocol=HTTP,
                                endpoint=host)

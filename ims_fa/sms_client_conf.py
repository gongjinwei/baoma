# -*- coding:UTF-8 -*-
import logging

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.protocol import HTTP

host = 'sms.bj.baidubce.com'
access_key_id ='331691219c464317ac1567d516ec6075'
secret_access_key =b'1f5c53505515416d91cdc275541d7403'

config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),protocol=HTTP,
                                endpoint=host)
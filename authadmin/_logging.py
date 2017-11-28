# -*- coding:UTF-8 -*-
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
    filename='logger.log',  # 默认输出到屏幕，如果有filename则会输出到文件中
    filemode='w'  # 默认是a追加模式
)

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')

# -*- coding:UTF-8 -*-
# 同时输出到屏幕和文件
import logging
from logging.handlers import HTTPHandler
import pymongo


# 自定义Handler

class MongoHandler(logging.Handler):
    def emit(self, record):
        pass


logger = logging.getLogger()
fh = logging.FileHandler('logger.log')  # 文件输出流的对象
ch = logging.StreamHandler()  # 标准输出流，用于输出到控制台
nw = HTTPHandler('localhost:8888', url='/')  # 默认以GET方式输出到网页上
formatter = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                              datefmt='%Y%m%d %H:%M:%S')

logger.setLevel('DEBUG')

fh.setFormatter(formatter)
ch.setFormatter(formatter)
nw.setFormatter(formatter)

logger.addHandler(fh)  # 输出到文件
logger.addHandler(ch)  # 输出到屏幕
logger.addHandler(nw)  # GET带参数输出

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')

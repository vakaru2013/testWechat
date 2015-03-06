# coding=utf-8

# 这个模块提供一个函数，这个函数返回一个用于写日志的对象，该对象类似于Python标准库中的logger对象

import logging
from bae_log import handlers

# 函数参数是日志对应的模块名字
def getLogger(moduleName):
    loghandler = handlers.BaeLogHandler(ak = "2p3CYGACdPhU1wXMRpsZXzdG", sk = "lGL8Kshw073T6Yspb9SV9zzsS4FGELAh", bufcount = 1)
    logger=logging.getLogger(moduleName)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(loghandler)
    return logger

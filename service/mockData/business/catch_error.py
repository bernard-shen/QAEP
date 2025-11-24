#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

import traceback
from loguru import logger
# import datetime


def CatchError(func):
    def wrapper(*args, **kwargs):
        try:
            logger.info('----{}:程序开始执行：...'.format(func.__name__))
            res = func(*args, **kwargs)
            logger.info('----{}:程序执行成功：...'.format(func.__name__))
            return res
        except Exception as e:
            logger.error("----{}:程序执行失败：报错信息如下：\n{}".format(func.__name__, e.args))
            traceback_info = traceback.format_exc()
            print(traceback_info)
    return wrapper


# @CatchError
# def sum(a,b):
#     return a + b

if __name__ == '__main__':
    pass
    # print(sum("asdf",3))


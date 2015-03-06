# coding=utf-8

import commondef

import baelogging
logger=baelogging.getLogger(__name__)

from handlerforinitstate import HandlerForInitState

# 这个函数返回一个handler，也可能发生错误返回的是None，handler的push函数以及两个属性是需要关心的。
def getHandlerForUser(userid):
    state=commondef.getUserState(userid)
    
    handlerMap={
        commondef.initState : HandlerForInitState(userid)
    }

    handler=handlerMap.get(state)
    if handler==None:
        # 有意外发生，记录日志
        logger.debug('current state is %s, error hanppen in getHandlerForUser', state)
    return handler
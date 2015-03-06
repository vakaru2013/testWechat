# coding=utf-8

import commondef

import baelogging
logger=baelogging.getLogger(__name__)

from handlerforinitstate import HandlerForInitState
from handlerforintrostate import HandlerForIntroState

# 这个函数返回一个handler，也可能发生错误返回的是None，handler的push函数以及两个属性是需要关心的。
def getHandlerForUser(xmlDict):
    userid=xmlDict[u'FromUserName']
    state=commondef.getUserState(userid)
    
    handlerMap={
        # 这是处理初始状态的handler
        commondef.initState : HandlerForInitState(userid),
        commondef.toRecvIntroState : HandlerForIntroState(userid,u'Content'])
    }

    handler=handlerMap.get(state)
    if handler==None:
        # 有意外发生，记录日志
        logger.debug('current state is %s, error hanppen in getHandlerForUser', state)
        # 重置用户的状态
        logger.debug('state has been reset in getHandlerForUser')
        commondef.setUserState(userid,commondef.initState)
    return handler
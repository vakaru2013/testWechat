# coding=utf-8

import baelogging
logger=baelogging.getLogger(__name__)

from baeredis import redisConn

# 这个模块定义了一些公用函数、字符串常量

# 下面是根据用户的id组装'在redis数据库存储用户状态的key'的函数
def makeUserStateKey(userid):
    return 'userState-%d' % userid
    
# 下面是根据用户的id组装'在redis数据库存储用户自我介绍的key'的函数
def makeUserIntroKey(userid):
    return 'userIntro-%d' % userid

# 下面是用户所处的状态的值，是一些字符串常量：
initState='init'
toRecvIntroState='to_recv_intro'
toRecvCmdState='to_recv_cmd'

# 下面是回复给微信客户端的text文本，是一些字符串常量
msgWaitForIntro=u'你还没有填写自我介绍，请发送你的自我介绍。'
msgWaitForCmd=u'你当前的自我介绍是：%s。想修改自我介绍请发送1，想查看在线用户资料请发送2，想检查你的收件箱请发送3。'
msgError=u'遇到了未知的错误'

# 这个函数从redis数据库中读取用户的状态
def getUserState(userid):
    key=makeUserStateKey(userid)
    state=redisConn.get(key)
    if state==None:
        state=initState
    return state
    
# 这个函数在redis数据库中设置用户的状态
def setUserState(userid,state):
    key=makeUserStateKey(userid)
    redisConn.set(key,state)
    
# 这个函数从redis数据库中读取用户的自我介绍，如果没有自我介绍，则返回None
def getUserIntro(userid):
    key=makeUserIntroKey(userid)
    intro=redisConn.get(key)
    return intro
    
# 这个函数在redis数据库中设置用户的自我介绍
def setUserIntro(userid,intro):
    key=makeUserIntroKey(userid)
    redisConn.set(key,intro)
    
# coding=utf-8

from handlerfactory import getHandlerForUser
import commondef

# 这个函数根据xmlDict返回要回复的响应消息，是unicode字符串
# xmlDict是字典，xml中的每个element的名字都是一个key，element的text是对应的value
def onRecvMsg(xmlDict):
    userid=xmlDict[u'FromUserName']
    handler=getHandlerForUser(userid)
    if handler==None:
        return commondef.msgError
    handler.push()
    
    # 修改用户在服务器中的状态，并返回响应字符串
    commondef.setUserState(userid,handler.state)
    return handler.rtext
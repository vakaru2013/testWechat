# coding=utf-8

import commondef

# 这个class提供push函数，push函数可以决定用户在服务器中的下一个状态，并组装一个响应给客户端的文本
class HandlerForInitState:
    
    # 接收用户的id作为参数
    def __init__(self,userid):
        self.userid=userid
        self.state=commondef.initState
        self.rtext=commondef.msgWaitForIntro
        
    # push函数可以决定用户在服务器中的下一个状态，并组装一个响应给客户端的文本
    def push(self):
        intro=commondef.getUserIntro(self.userid)
        if intro==None:
            # 要求用户发送自我介绍
            self.state=commondef.toRecvIntroState
            self.rtext=commondef.msgWaitForIntro
        else:
            # 用户已经有自我介绍了，要求用户发送命令
            self.state=commondef.toRecvCmdState
            self.rtext=commondef.msgWaitForCmd % intro
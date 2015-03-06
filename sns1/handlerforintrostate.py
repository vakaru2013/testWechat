# coding=utf-8

import commondef

# 这个class提供push函数，push函数可以决定用户在服务器中的下一个状态，并组装一个响应给客户端的文本
class HandlerForIntroState:
    
    # 接收用户的id作为参数
    def __init__(self,userid,intro):
        self.userid=userid
        self.intro=intro
        self.state=commondef.initState
        self.rtext=commondef.msgWaitForIntro
        
    # 这个函数将状态修改为to recv cmd，并记录发来的自我介绍
    def push(self):
        self.state=commondef.toRecvCmdState
        self.rtext=commondef.msgWaitForCmd % self.intro
        commondef.setUserIntro(self.userid,self.intro)
    
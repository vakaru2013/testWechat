# coding=utf-8

import commondef

# 这个class提供push函数，push函数可以决定用户在服务器中的下一个状态，并组装一个响应给客户端的文本
class HandlerForCmdState:
    
    # 接收用户的id作为参数
    def __init__(self,userid,cmd):
        self.userid=userid
        self.cmd=cmd
        self.state=commondef.initState
        self.rtext=commondef.msgWaitForIntro
        
    # 这个函数根据cmd的值来执行不同的行为。
    def push(self):
        if self.cmd==u'1':
            # 用户想要修改自我介绍
            self.state=commondef.toRecvIntro
            self.rtext=commondef.msgWaitForIntro
        elif self.cmd==u'2':
            # 用户想要查看其他用户的资料
        elif self.cmd==u'3':
            # 用户想要检查收件箱
        else:
            self.state=commondef.toRecvCmdState
            self.rtext=commondef.msgWaitForCmd % self.intro
    
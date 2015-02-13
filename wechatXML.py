#-*- coding:utf-8 -*-

from xml.sax import *

class WechatXmlHandler(handler.ContentHandler):
    
    def __init__(self):
        self.current_=''
        self.content_={}
    
    def startElement(self,name,attrs):
        # <xml>
        # <ToUserName><![CDATA[toUser]]></ToUserName>
        # <FromUserName><![CDATA[fromUser]]></FromUserName> 
        # <CreateTime>1348831860</CreateTime>
        # <MsgType><![CDATA[text]]></MsgType>
        # <Content><![CDATA[this is a test]]></Content>
        # <MsgId>1234567890123456</MsgId>
        # </xml>
        
        # 我要用字典来替代if else的用法，但在这个函数里，连字典都不需要
        # if(name=="ToUserName"):
        #     self.current_='ToUserName'
        # else if(name=="FromUserName"):
        #     self.current_='FromUserName'
        # else if(name=="CreateTime"):
        #     self.current_='CreateTime'
        # else if(name=="MsgType"):
        #     self.current_='MsgType'
        # else if(name=="Content"):
        #     self.current_='Content'
        # else if(name=="MsgId"):
        #     self.current_='MsgId'
        # else
        #     self.current_=''

        self.current_=name
        
    def characters(self,content):
        
        
        # 通过测试发现，微信的这个xml的格式是非常不标准的，因为一个element可能多次出来character，当然后面的是空的。
        # 并且不知道为什么，用parsePlain就能够直接得到想要的内容
        
        #这个函数是默认函数，什么也不做
        def parseDef(current,text):
            return
        
        def parsePlain(current,text):
            # text本身就是内容
            if(self.content_.get(current,'')==''):
                print 'current:',current,', text:',text
                self.content_[current]=text
            
        #下面是利用字典来实现switch，以替代Python的if else语句，print是默认的函数对象。
        # 将内容都保存到content_属性中
        {
            'ToUserName':parsePlain,
            'FromUserName':parsePlain,
            'MsgType':parsePlain,
            'Content':parsePlain,
            'CreateTime':parsePlain,
            'MsgId':parsePlain
        }.get(self.current_,parseDef)(self.current_,content)
        
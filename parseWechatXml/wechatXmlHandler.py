#-*- coding:utf-8 -*-

# 该文件提供WechatXmlHandler类，它的实例可以喝xml.sax.parse函数一起使用，如下
# hdl=WechatXmlHandler()
# parse('test.xml',hdl)

from xml.sax import *

import logging
from bae_log import handlers

loghandler = handlers.BaeLogHandler(ak = "2p3CYGACdPhU1wXMRpsZXzdG", sk = "lGL8Kshw073T6Yspb9SV9zzsS4FGELAh", bufcount = 1)
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(loghandler)

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

        self.current_=name
        
        if isinstance(name,str):
            logger.debug('name argument of startElement method of handler.ContentHandler is 8 bit string.')
        if isinstance(name,unicode):
            logger.debug('name argument of startElement method of handler.ContentHandler is unicode string.')
        
    def characters(self,content):
        
        if isinstance(content,str):
            logger.debug('content argument of characters method of handler.ContentHandler is 8 bit string.')
        if isinstance(content,unicode):
            logger.debug('content argument of characters method of handler.ContentHandler is unicode string.')
        
        # 通过测试发现，微信的这个xml的格式是非常不标准的，因为一个element可能多次出来character，当然后面的是空的。
        # 并且不知道为什么，用parsePlain就能够直接得到想要的内容
        
        #这个函数是默认函数，什么也不做
        def parseDef(current,text):
            return
        
        def parsePlain(current,text):
            # text本身就是内容
            if(self.content_.get(current,'')==''):
                # 通过测试发现，微信的这个xml的格式是非常不标准的，因为一个element可能多次出来character，当然后面的是空的。
                # 所以我在这里检查它是否是空，仅当是空才处理
                
                # print(text)这个会异常，而print(text.encode('utf-8'))不会异常，这个和文档中下面所描述的不同，想不通为什么
                # To print or display some strings properly, they need to be decoded (Unicode strings).                
                
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
        
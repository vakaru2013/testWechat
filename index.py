#-*- coding:utf-8 -*-

from cgi import parse_qs, escape
from hashlib import sha1

# 解析微信的xml格式的handler
from parseWechatXml.wechatXmlHandler import *

import time

import logging
from bae_log import handlers
handler = handlers.BaeLogHandler(ak = "2p3CYGACdPhU1wXMRpsZXzdG", sk = "lGL8Kshw073T6Yspb9SV9zzsS4FGELAh", bufcount = 256)
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.fatal("fatal message")
logger.log(12, "trace message")
        
def app(environ, start_response):
    
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    
    if('GET'==environ.get('REQUEST_METHOD','')):
        # 取出query string的值
        # 检查是否是微信的echostr
        qs=environ.get('QUERY_STRING','')
        # d是一个字典，每个键是query string中的一个键，值是一个list，因为在query string中可能有相同名字的键所有有多个值
        d = parse_qs(qs)
        # query string里还有signature，timestamp，nonce，另外我这个微信公众号的token是hello
        # 校验此消息是否来自微信
        # 加密/校验流程如下：
        # 1. 将token、timestamp、nonce三个参数进行字典序排序
        # 2. 将三个参数字符串拼接成一个字符串进行sha1加密
        # 3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        token='hello'
        echostr = escape(d.get('echostr', [''])[0])
        timestamp = escape(d.get('timestamp', [''])[0])
        nonce = escape(d.get('nonce', [''])[0])
        signature = escape(d.get('signature', [''])[0])
        # sha1是一个类型
        temp=[token,timestamp,nonce]
        temp.sort()
        temp=''.join(temp)
        temp=sha1(temp).hexdigest()
        
        if(signature==temp):
            # 这是微信发来的消息，所以返回echostr
            start_response(status, headers)
            return [echostr]

    if('POST'==environ.get('REQUEST_METHOD','')):    
        # the environment variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
            
        # 这就是微信发来的消息的消息体
        logger.debug('request body size: %d', request_body_size)
        request_body=environ['wsgi.input'].read(request_body_size)
        logger.debug(request_body)
        
        # <xml>
        # <ToUserName><![CDATA[toUser]]></ToUserName>
        # <FromUserName><![CDATA[fromUser]]></FromUserName> 
        # <CreateTime>1348831860</CreateTime>
        # <MsgType><![CDATA[text]]></MsgType>
        # <Content><![CDATA[this is a test]]></Content>
        # <MsgId>1234567890123456</MsgId>
        # </xml>
        
        # 解析xml
        hdl=WechatXmlHandler()
        parseString(request_body,hdl)
        
        
        # 解析出消息的内容
        # 编辑回复消息文本，回复
        # <xml>
        # <ToUserName><![CDATA[toUser]]></ToUserName>
        # <FromUserName><![CDATA[fromUser]]></FromUserName>
        # <CreateTime>12345678</CreateTime>
        # <MsgType><![CDATA[text]]></MsgType>
        # <Content><![CDATA[你好]]></Content>
        # </xml>
        
        reply=( u'<xml>'
                u'<ToUserName><![CDATA[{0}]]></ToUserName>'
                u'<FromUserName><![CDATA[{1}]]></FromUserName>'
                u'<CreateTime>{2}</CreateTime>'
                u'<MsgType><![CDATA[text]]></MsgType>'
                u'<Content><![CDATA[{3}]]></Content>'
                u'</xml>' )

        # rtext='hello world!'
        # if(hdl.content_['Content']=='我是宁宁'):
        #     rtext='我是宋伟'
        rtext=hdl.content_['Content']

        # 中文导致异常？
        # 因为wsgi.input通过read函数给出来的已经是Python的unicode字符串了，假如前面的reply变量字符串不是unicode而是Python的8bit的字符串，
        # 那么这里的format函数就会要把参数encode为8bit的字符串，用默认的ASCII codec，ASCII codec不认识中文字符，所以异常。
        # 如果reply是unicode字符串，就不需要encode，就不会异常了，
        reply=reply.format(hdl.content_['FromUserName'],hdl.content_['ToUserName'],int(time.time()),rtext)
        
        # 指定为xml，消息体为utf-8编码，
        headers = [('Content-type', 'text/xml')]
        start_response(status, headers)
        return [reply.encode('utf-8')]
        
    # 下面的调试代码能够将environ中的所有的键值对都输出，仅用于调试目的
    body=[str(environ)]
    start_response(status, headers)
    return body
        
    # 如果上面的情况都不是，就返回下面的字符串
    body=["Welcome to Baidu Cloud!\n This is test.py!\n"]
    start_response(status, headers)
    return body

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

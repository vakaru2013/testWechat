#-*- coding:utf-8 -*-

from cgi import parse_qs, escape
from hashlib import sha1

# 解析微信的xml格式的handler
from wechatXML import *

import time
        
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
        request_body=environ['wsgi.input'].read(request_body_size)
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
        
        reply=( '<xml>'
                '<ToUserName><![CDATA[{0}]]></ToUserName>'
                '<FromUserName><![CDATA[{1}]]></FromUserName>'
                '<CreateTime>{2}</CreateTime>'
                '<MsgType><![CDATA[text]]></MsgType>'
                '<Content><![CDATA[{3}]]></Content>'
                '</xml>' )
        reply=reply.format(hdl.content_['FromUserName'],hdl.content_['ToUserName'],int(time.time()),"hello world!")
        
        # 指定为xml，并且指定为utf-8编码，以防止乱码
        headers = [('Content-type', 'text/xml')]
        start_response(status, headers)
        return [reply]
        
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

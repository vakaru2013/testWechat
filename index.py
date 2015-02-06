#-*- coding:utf-8 -*-

from cgi import parse_qs, escape
from hashlib import sha1

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    
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
        echostr = d.get('echostr', [''])[0]
        timestamp = d.get('timestamp', [''])[0]
        nonce = d.get('nonce', [''])[0]
        signature = d.get('signature', [''])[0]
        # sha1是一个类型
        temp=[token,timestamp,nonce]
        temp=temp.sort()
        if(signature==sha1(''.join(temp)).hexdigest()):
            # 这是微信发来的消息，所以返回echostr
            return [echostr]
    
    # 下面的调试代码能够将environ中的所有的键值对都输出，仅用于调试目的
    body=[str(environ)]
    return body

    if('POST'==environ.get('REQUEST_METHOD','')):    
        # the environment variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body=environ['wsgi.input'].read(request_body_size)
        return [request_body]
        
    # 如果上面的情况都不是，就返回下面的字符串
    body=["Welcome to Baidu Cloud!\n This is test.py!\n"]
    return body

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

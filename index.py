#-*- coding:utf-8 -*-

from cgi import parse_qs, escape

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    
    # 取出query string的值
    # Returns a dictionary containing lists as values.
    # 检查是否是微信的echostr
    d = parse_qs(environ['QUERY_STRING'])
    echostr = d.get('echostr', []) # Returns a list of echostr.
    if(len(echostr)>0):
        # 是，直接返回该字符串
        return [echostr[0]]
    
    # 检查是否是微信发来的文本消息，是POST消息，且是XML数据包
    # 下面的调试代码能够将environ中的所有的键值对都输出
    body=[str(environ)]
    return body
    
    # 如果上面的情况都不是，就返回下面的字符串
    body=["Welcome to Baidu Cloud!\n This is test.py!\n"]
    return body

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

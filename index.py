#-*- coding:utf-8 -*-

from cgi import parse_qs, escape

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    
    # 取出query string的值
    # Returns a dictionary containing lists as values.
    d = parse_qs(environ['QUERY_STRING'])
    echostr = d.get('echostr', []) # Returns a list of echostr.
    if(len(echostr)>0):
        return [echostr[0]]
    
    # 如果query string中没有echostr就返回下面的字符串
    body=["Welcome to Baidu Cloud!\n This is test.py!\n"]
    return body

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

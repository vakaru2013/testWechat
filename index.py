#-*- coding:utf-8 -*-

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    body=["Welcome to Baidu Cloud!\n"]
    
    # 遍历environ字典
    inputs=["%s==%s" % (k,x) for (k,x) in environ.items()]
    
    # 将environ中所有的键值对输出
    body+=inputs
    body='\r\n\r\n'.join(body)
    return [body]

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

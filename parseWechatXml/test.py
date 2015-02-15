# -*- coding: utf-8 -*-

import time

from wechatXmlHandler import *
hdl=WechatXmlHandler()


# 测试parse字符串
hdl2=WechatXmlHandler()
parseString('<xml><ToUserName><![CDATA[你好]]></ToUserName></xml>',hdl2)

# 测试parse文件
parse('test.xml',hdl)

reply=( '<xml>'
        '<ToUserName><![CDATA[{0}]]></ToUserName>'
        '<FromUserName><![CDATA[{1}]]></FromUserName>'
        '<CreateTime>{2}</CreateTime>'
        '<MsgType><![CDATA[text]]></MsgType>'
        '<Content><![CDATA[{3}]]></Content>'
        '</xml>'
        )


# 这个文件存储时用的字符编码是 Unicode-utf-8
# 但是我们要告诉Python解释器这个文件的字符编码是 Unicode-utf-8，因为Python文件是纯文本文件，它在存储的时候并没有额外的说它的编码方式。
# Python解释器是一个字节一个字节的来读的，而它默认认为字符编码是ASCII，所以如果遇到非ASCII字节，它就挂了，比如遇到 Non-ASCII character '\xe5'

# When you specify # -*- coding: utf-8 -*-, you're telling Python the source file you've saved is utf-8. The default for Python 2 is ASCII (for Python 3 it's utf-8)




# 微信的发来的xml的格式做的一个xml文件 — test.xml
# 一个定义了xml.sax.handler.contentHandler的子类的py文件 — wechatXmlHandler.py
# 一个py文件，利用xml.sax.parse()函数，用handler来parse test.xml，并且：
# 它还会利用解析出来的信息构造一个符合微信平台要求的返回给微信的xml字符串。
# 这是一个测试文件 — test.py
#
# 运行test.py后，期待的执行结果：
# 打印出构造出来的reply。
# 如果没有异常，
# 且reply的内容与test.xml中的内容能够对应起来，基本上就是对的。所以，需要检查
# 1，是否有异常，
# 2，如果仔细点的，需要检查reply的内容中的tousername与fromusername是否与test.xml中的刚好相反
# 3，检查content是否与test.xml宗的相同。        
reply=reply.format(hdl.content_['FromUserName'],hdl.content_['ToUserName'],int(time.time()),"hello world!")

print reply
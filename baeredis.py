# coding=utf-8

# 这个模块提供一个函数，这个函数返回一个与redis数据库的连接。

### 开发者在requirements.txt中指定依赖redis使用
import redis

### 请在管理控制台获取host, port, db_name, api_key, secret_key的值 
db_name = "JGVOMTQdfGqgSryqehLI"
api_key = "2p3CYGACdPhU1wXMRpsZXzdG"
secret_key = "lGL8Kshw073T6Yspb9SV9zzsS4FGELAh"
myauth = "%s-%s-%s"%(api_key, secret_key, db_name)

### 连接redis服务
def connectRedis():
    r = redis.Redis(host = "redis.duapp.com", port = 80, password = myauth)
    return r
    
# 给其他模块提供下面这个对象redisConn
redisConn=baeredis.connectRedis()
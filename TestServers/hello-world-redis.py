#!/usr/bin/env python3
# docker run -d --rm --name REDIS -p 6379:6379 redis:alpine
# docker exec -it REDIS redis-cli - obrir client de REDIS
# execute this file to know if it's working
# docker stop REDIS (or your docker name)

import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""


def hello_redis():
    
    try:

        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    
        r.set("msg:hello", "Hello Redis!!!")

        msg = r.get("msg:hello")
        print(msg)        
    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    hello_redis()

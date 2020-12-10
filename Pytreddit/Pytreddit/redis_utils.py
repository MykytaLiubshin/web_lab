from django.conf import settings
import redis


class RedisMngr:
    def __init__(self, _host=None, _port=None):
        self.host = settings.REDIS_HOST if _host is None else _host
        self.port = settings.REDIS_PORT if _port is None else _port
        self.redis_instance = redis.StrictRedis(
            host=self.host, port=self.port, db=0
        )

    def Rget(self, key):
        return self.redis_instance.get(key)

    def Rput(self, key, val):
        return self.redis_instance.set(key, val)

    def Rdelete(self, key):
        return self.redis_instance.delete(key)


REDIS_MN = RedisMngr()

def get_redis_instance():
    return REDIS_MN

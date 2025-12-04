import os
from django_redis import get_redis_connection


class RedisOtp:
    def __init__(self):
        self.url = os.getenv("REDIS_URL", "redis://localhost:6381/1")

    def connect_redis():
        pass

    def tearDown(self):
        get_redis_connection("default").flushall()

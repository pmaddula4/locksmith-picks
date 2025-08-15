import redis
import os

def get_redis():
    return redis.Redis(
        host=os.environ.get("REDIS_HOSTNAME"),
        port=6380,
        password=os.environ.get("REDIS_PASSWORD"),
        ssl=True
    )

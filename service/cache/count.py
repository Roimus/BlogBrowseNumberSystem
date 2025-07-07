import redis
from django.conf import settings


class ViewCountCache:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        self.key = "article:number"

    # 看的数量增加
    def add(self, article_id: int):
        try:
            return self.client.hincrby(self.key, str(article_id), 1)
        except redis.RedisError as e:
            raise Exception(f"Redis操作失败: {str(e)}")

    # 获取数量
    def get(self, article_id: int):
        try:
            value = self.client.hget(self.key, str(article_id))
            return int(value) if value else 0
        except redis.RedisError as e:
            raise Exception(f"Redis操作失败: {str(e)}")
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
        self.stats_key = "cache:stats"
        # 一进来就初始化
        self.init_redis_cache()
    
    # 计算一下有多少次是成功进入缓存的
    def init_redis_cache(self):
        if not self.client.exists(self.stats_key):
            stats = {
                "成功": 0,
                "丢失": 0,
                "总的": 0
            }
            self.client.hmset(self.stats_key, stats)
    
    # 每次使用增加浏览量后都更新一下缓存
    def update_cache_stats(self, hit: bool):
        pipe = self.client.pipeline()
        pipe.hincrby(self.stats_key, "总的", 1)
        if hit:
            pipe.hincrby(self.stats_key, "成功", 1)
        else:
            pipe.hincrby(self.stats_key, "丢失", 1)
        pipe.execute()

    # 看的数量增加
    def add(self, article_id: int):
        try:
            result = self.client.hincrby(self.key, str(article_id), 1)
            self.update_cache_stats(hit=True)
            return result
        except redis.RedisError as e:
            raise Exception(f"Redis操作失败: {str(e)}")

    # 获取数量
    def get(self, article_id: int):
        try:
            value = self.client.hget(self.key, str(article_id))
            # 每一次的都要更新一下缓存
            if value is not None:
                self.update_cache_stats(hit=True)
                return int(value)
            else:
                self.update_cache_stats(hit=False)
                return 0
                
        except redis.RedisError as e:
            self.update_cache_stats(hit=False)
            raise Exception(f"Redis操作失败: {str(e)}")
    
    # 计算一下命中率
    def get_cache_hit_rate(self):
        stats = self.client.hgetall(self.stats_key)
        total_requests = int(stats.get("总的", 0))
        hits = int(stats.get("成功", 0))
        misses = int(stats.get("丢失", 0))
        
        hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "总的": total_requests,
            "成功": hits,
            "丢失": misses,
            "命中率": round(hit_rate, 2)
        }
    
    # 重置一下缓存数据
    def reset_cache_stats(self):
        self.client.hset(self.stats_key, "总的", 0)
        self.client.hset(self.stats_key, "成功", 0)
        self.client.hset(self.stats_key, "丢失", 0)
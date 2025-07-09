from service.cache.count import ViewCountCache
from service.dao.article_mysql import ArticleMysql
from service.tasks import update_mysql_number
import redis

class ViewCountService:

    def query_number(self, article_id: int):
        try:
            count = ViewCountCache().get(article_id)
            return count
        # 拿不到就从数据库拿，可以降级处理
        except (redis.RedisError, ConnectionError) as e:
            try:
                count = ArticleMysql().query_number(article_id)
                # 然后把数据放回redis里面
                try:
                    ViewCountCache().client.hset(ViewCountCache().key, article_id, count)
                except Exception as cache_error:
                    return count
            except Exception as db_error:
                return 0
        except Exception as e:
            try:
                count = ArticleMysql().query_number(article_id)
                return count
            except Exception as db_error:
                return 0

    def add_number(self, article_id: int):
        try:
            new_count = ViewCountCache().add(article_id)
            # 缓存后就更新数据库
            try:
                update_mysql_number.delay(article_id, new_count)
            except Exception as async_error:
                print(async_error)
            return new_count
        # 缓存不行就数据库
        except (redis.RedisError, ConnectionError) as e:
            print(e)
            try:
                return ArticleMysql().add_number(article_id)
            except Exception as db_error:
                print(db_error)
                return -1 
        except Exception as e:
            print(e)
            try:
                return ArticleMysql().add_number(article_id)
            except Exception as db_error:
                print(db_error)
                return -1
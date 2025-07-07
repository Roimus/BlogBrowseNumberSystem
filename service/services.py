from service.cache.count import ViewCountCache
from service.dao.article_mysql import ArticleMysql
from service.tasks import update_mysql_number

class ViewCountService:

    def query_number(self, id: int):
        try:
            count = ViewCountCache().get(id)
            return count
        # 如果缓存拿不到
        except Exception as e:
            print(str(e))
            count = ArticleMysql().query_number(id)
            # 放回缓存
            try:
                ViewCountCache().client.hset(ViewCountCache().key, id, count)
            except Exception:
                return count

    def add_number(self, id: int):
        try:
            new_count = ViewCountCache().add(id)
            # 通过异步将缓存中的数量存入数据库
            update_mysql_number.delay(id, new_count)
            return new_count
        except Exception as e:
            return ArticleMysql().add_number(id)
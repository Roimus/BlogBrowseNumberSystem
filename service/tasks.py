from celery import shared_task
from service.cache.count import ViewCountCache
from article.models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, OperationalError


@shared_task(bind=True, max_retries=3)
def update_mysql_number(self, article_id: int, count: int):

    try:
        # 找到该文章 保存数量
        article = Article.objects.get(pk=article_id)
        article.count = count
        article.save()

        # 看看缓存和数据库内容是否一致
        try:
            cached_count = ViewCountCache().get(article_id)
            if cached_count != count:
                print("不一致")
        except Exception as cache_error:
            print("缓存验证失败")
            
    except Exception as e:
        print(e)
        return False



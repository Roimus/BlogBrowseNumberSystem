from celery import shared_task
from service.cache.count import ViewCountCache
from article.models import Article


@shared_task(bind=True, max_retries=3)
def update_mysql_number(self, article_id: int, count: int):

    try:
        # 找到该文章 保存数量
        article = Article.objects.get(pk=article_id)
        article.view_count = count
        article.save()

        cached_count = ViewCountCache().get(article_id)
        if cached_count != count:
            raise Exception('缓存和数据库中的观看数量不一样')
    except Exception as e:
        raise Exception(str(e))


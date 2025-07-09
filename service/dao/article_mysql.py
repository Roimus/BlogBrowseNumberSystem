from article.models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, OperationalError


class ArticleMysql:
    def query_number(self, article_id: int):
        try:
            article = Article.objects.get(pk=article_id)
            return article.count
        except Exception as e:
            print(f"发生错误: {e}")
            raise Exception(f"查询失败: {str(e)}")

    def add_number(self, article_id: int):
        try:
            article = Article.objects.get(pk=article_id)
            article.count += 1
            article.save()
            return article.count
        except Exception as e:
            print(f"发生错误: {e}")
            raise Exception(f"增加失败: {str(e)}")
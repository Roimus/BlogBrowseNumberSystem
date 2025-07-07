from article.models import Article


class ArticleMysql:
    def query_number(self, article_id: int):
        try:
            article = Article.objects.get(pk=article_id)
            return article.count
        except Exception as e:
            raise Exception(f"查询观看数量失败: {str(e)}")

    def add_number(self, article_id: int):
        try:
            article = Article.objects.get(pk=article_id)
            article.count += 1
            article.save()
            return article.count
        except Exception as e:
            raise Exception(f"增加观看数量失败: {str(e)}")
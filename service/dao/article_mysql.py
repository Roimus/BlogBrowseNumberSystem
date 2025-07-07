from article.models import Article


class ArticleMysql:
    def query_number(self, id: int):
        try:
            article = Article.objects.get(pk=id)
            return article.count
        except Exception as e:
            raise Exception(f"查询观看数量失败: {str(e)}")

    def add_number(self, id: int):
        try:
            article = Article.objects.get(pk=id)
            article.count += 1
            article.save()
            return article.count
        except Exception as e:
            raise Exception(f"增加观看数量失败: {str(e)}")
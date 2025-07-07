from django.core.management.base import BaseCommand
from article.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = [
            {"title": "测试1", "content": "666"},
            {"title": "测试2", "content": "这是测试2"},
            {"title": "测试3", "content": "这才是3"}
        ]

        for article in articles:
            Article.objects.create(**article)
            self.stdout.write(f'创建表: {article["title"]}')

        self.stdout.write(self.style.SUCCESS('创建成功'))
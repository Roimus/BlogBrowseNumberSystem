from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50) # 标题最长50
    content = models.TextField()
    count = models.IntegerField(default=0) # 从redis中拿过来
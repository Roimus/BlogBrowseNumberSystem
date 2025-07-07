from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from service.services import ViewCountService
from models import Article


def article_add(request, id):
    article = get_object_or_404(Article, pk=id)

    service = ViewCountService()
    number = service.add_number(id)

    return JsonResponse({
        'title': article.title,
        'content': article.content,
        'number': number
    })
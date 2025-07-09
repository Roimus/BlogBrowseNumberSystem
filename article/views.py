from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from service.services import ViewCountService
from .models import Article
from service.cache.count import ViewCountCache


def article_add(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    service = ViewCountService()
    number = service.add_number(article_id)

    return JsonResponse({
        'title': article.title,
        'content': article.content,
        'number': number
    })


def get_cache(request):
    try:
        cache = ViewCountCache()
        stats = cache.get_cache_hit_rate()
        
        return JsonResponse({'success': True,'data': stats})
    except Exception as e:
        return JsonResponse({'success': False,'error': str(e)}, status=500)


def reset_cache(request):
    try:

        cache = ViewCountCache()
        cache.reset_cache_stats()
        
        return JsonResponse({'success': True,'message': '重置成功'})
    except Exception as e:
        return JsonResponse({'success': False,'error': str(e)}, status=500)
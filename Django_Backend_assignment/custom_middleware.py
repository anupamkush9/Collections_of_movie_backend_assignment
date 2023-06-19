from accounts.models import RequestCounter
from django.http import JsonResponse
from django.db.models import F


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/request-count/reset/' and request.method == 'POST':
            RequestCounter.objects.update(count=0)
            return JsonResponse({'message': 'Request count reset successfully'})

        request_counter, created = RequestCounter.objects.get_or_create(pk=1)
        request_counter.count = F('count') + 1
        request_counter.save()

        if request.path == '/request-count/' and request.method == 'GET':
            request_count = RequestCounter.objects.values('count').get(pk=1)['count']
            return JsonResponse({'requests': request_count})

        response = self.get_response(request)
        return response

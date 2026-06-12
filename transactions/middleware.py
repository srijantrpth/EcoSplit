from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path=='/api/expenses/' and request.method=='POST':
            ip_address = request.META.get('REMOTE_ADDR')
            cache_key = f"rate_limit_{ip_address}"
            request_count = cache.get(cache_key, 0)
            if request_count>=5:
                return JsonResponse({"error": "Too Many Requests! Wait a Minute! "}, status=429)
            else:
                request_count+=1
                cache.set(cache_key, request_count, 60)
        response=self.get_response(request)
        return response


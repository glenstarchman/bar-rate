from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class AddRequestTimestamp(MiddlewareMixin):

    def process_request(self, req):
        now = timezone.now()
        now_ms = now.timestamp() * 1000
        setattr(req, 'start_timestamp', now_ms)

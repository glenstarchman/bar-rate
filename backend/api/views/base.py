from rest_framework.response import Response
from django.utils import timezone


def build_response(request, data):
    """wrap a response with some basic metadata"""
    end_ts = timezone.now().timestamp() * 1000
    elapsed = end_ts - request.start_timestamp
    user = None
    if request.user.is_authenticated:
        user = {
            "username": request.user.username,
            "id": str(request.user.id),
        }

    resp = {
        'meta': {
            'user': user,
            'request_time': elapsed,
            'request_start': request.start_timestamp,
            'request_end': end_ts,
            'count': len(data),
        },
        'data': data,
    }

    return Response(resp)

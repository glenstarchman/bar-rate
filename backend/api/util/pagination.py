from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):

    def get_paginated_response(self, data):
        resp = {
            'meta': {
                'user': request.user.username,
                'request_time': str(timezone.now()),

            },
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
            },
            'data': data,
        }
        return Response(resp)

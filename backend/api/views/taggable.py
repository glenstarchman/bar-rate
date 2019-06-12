import json
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .base import build_response
from ..util import Pagination
from ..serializers.taggable_serializer import *


class TaggableViewSet(viewsets.ViewSet):
    pagination_class = Pagination
    paginate_by = 1
    paginate_by_param = 'page_size'
    max_paginate_by = 30

    SUCCESS = {
        'success': True
    }

    def _get_endpoint(self, request):
        p = request.path.split('/')
        path = ''
        if p[-1] == '':
            path = p[-2]
        else:
            path = p[-1]
        return path

    def get_taggable(self, request, pk, serializer):
        #this needs pagination
        obj = get_object_or_404(self.queryset, pk=pk)
        #determine which method to call
        path = self._get_endpoint(request)
        qs = getattr(obj, path)
        ser = serializer(qs, many=True)
        return build_response(request, ser.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        return self.get_taggable(request, pk, LikeSerializer)


    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        return self.get_taggable(request, pk, ReviewSerializer)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        return self.get_taggable(request, pk, CommentSerializer)

    @action(detail=True, methods=['get'])
    def tags(self, request, pk=None):
        return self.get_taggable(request, pk, TagSerializer)

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        return self.get_taggable(request, pk, ImageSerializer)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        user = request.user
        obj = get_object_or_404(self.queryset, pk=pk)
        obj.add_like(user=user)
        return build_response(request, self.SUCCESS)

    def toggle_with_body(self, request, pk=None):
        """either set or unset a taggable item"""
        user = request.user
        body_unicode = request.body.decode('utf-8')
        if body_unicode:
            body = json.loads(body_unicode)
        else:
            body = {}
        #now detemine which add_* method to call
        #note that in the case of like/dislike
        #the add function actually deletes, go figure
        body['user'] = user
        path = self._get_endpoint(request)
        method = "add_%s" % (path,)
        obj = get_object_or_404(self.queryset, pk=pk)
        func = getattr(obj, method)
        if body:
            func(**body)
        else:
            func()
        return build_response(request, self.SUCCESS)



    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    @action(detail=True, methods=['post'])
    def tag(self, request, pk=None):
        return self.toggle_with_body(request, pk)

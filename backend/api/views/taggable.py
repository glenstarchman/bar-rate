import json
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .base import build_response
from ..util import Pagination
from ..serializers.taggable_serializer import *
from ..serializers.mini_serializers import MiniUserSerializer


class TaggableViewSet(viewsets.ViewSet):
    """mix-in endpoints for all taggable objects:
       provides detail, list, create, and delete
       ex:
          GET /api/bar/1/likes/ -- list all likes for Bar 1
          POST /api/bar/1/like/ -- creates a like for bar 1
          DEL /api/bar/1/like/1/ -- delete the like with id 1 for bar 1
          GET /api/bar/1/like/1/ -- get the full detail of the like
          (*** NOT IMPLEMEMTED AND MAY NOT BE NEEDED ***)
    """
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
        #TODO: pagination!
        ser = serializer(qs, many=True)
        return build_response(request, ser.data)

    def delete_taggable(self, request):
        """delete a taggable, other than like"""
        pass

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None, id=None):
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

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        return self.get_taggable(request, pk, FollowerSerializer)

    def toggle_with_body(self, request, pk=None):
        """either set or unset a taggable item"""
        user = request.user
        body_unicode = request.body.decode('utf-8')
        if body_unicode:
            body = json.loads(body_unicode)
        else:
            body = {}
        #now determine which add_* method to call
        #note that in the case of like/dislike
        #the add function actually deletes, go figure
        body['user'] = user
        path = self._get_endpoint(request)
        method = "add_%s" % (path,)
        obj = get_object_or_404(self.queryset, pk=pk)
        func = getattr(obj, method)
        taggable = None
        if body:
            taggable = func(**body)
            return build_response(request, {'taggable_id': str(taggable.id)})
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

    @action(detail=True, methods=['post'], name='add-review')
    def review(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    @action(detail=True, methods=['post'], name='add-tag')
    def tag(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    @action(detail=True, methods=['post'], name='add-follower')
    def follower(self, request, pk=None):
        return self.toggle_with_body(request, pk)

    def delete_lookup(self, request, obj_model, pk, taggable_pk):
        main_obj = get_object_or_404(self.queryset, pk=pk)
        user = request.user
        taggable = get_object_or_404(obj_model, id=taggable_pk, user=user)
        print(taggable)
        obj_model.objects.filter(id=taggable_pk, user=user).delete()
        return build_response(request, self.SUCCESS)

    @action(detail=True, methods=['delete',], name='delete-like',
            url_path="like/(?P<like_id>[^/]+)")
    def delete_like(self, request, pk=None, like_id=None):
        return self.delete_lookup(request, Like, pk, like_id)

    @action(detail=True, methods=['delete',], name='delete-comment',
            url_path="comment/(?P<comment_id>[^/]+)")
    def delete_comment(self, request, pk=None, comment_id=None):
        return self.delete_lookup(request, Comment, pk, like_id)

    @action(detail=True, methods=['delete',], name='delete-follower',
            url_path="follower/(?P<follower_id>[^/]+)")
    def delete_follower(self, request, pk=None, follower_id=None):
        return self.delete_lookup(request, Follower, pk, follower_id)

    @action(detail=True, methods=['delete',], name='delete-tag',
            url_path="tag/(?P<tag_id>[^/]+)")
    def delete_tag(self, request, pk=None, tag_id=None):
        return self.delete_lookup(request, Tag, pk, tag_id)

    @action(detail=True, methods=['delete',], name='delete-review',
            url_path="review/(?P<review_id>[^/]+)")
    def delete_review(self, request, pk=None, review_id=None):
        return self.delete_lookup(request, Review, pk, review_id)

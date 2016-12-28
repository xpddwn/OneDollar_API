# coding:utf-8
from collections import OrderedDict

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        try:
            previous = self.page.previous_page_number()
        except:
            previous = None
        try:
            next_page = self.page.next_page_number()
        except:
            next_page = None
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', next_page),
            ('previous', previous),
            ('results', data),
        ]))


class ModelViewSet(generics.GenericAPIView):
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        if request.GET.get(u'id'):
            queryset = queryset.filter(id=request.GET.get(u'id'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        print page
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# coding:utf-8
from rest_framework import filters
from django.db.models import Q
from sku.models import Goods
import json
import django_filters


class JsonOrderingFilter(filters.OrderingFilter):
    ordering_param = 'order_by'

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            try:
                fields = json.loads(params)
            except ValueError:
                return self.get_default_ordering(view)

            ordering = self.remove_invalid_fields(queryset, fields, view)
            if ordering:
                return ordering

        return self.get_default_ordering(view)


class JsonDjangoFilterBackend(filters.DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)
        params = request.query_params.get('filters')
        if not params:
            return queryset

        try:
            filter_params = json.loads(params)
        except (ValueError, TypeError):
            return queryset

        if filter_class:
            return filter_class(filter_params, queryset=queryset).qs

        return queryset


class JsonSearchFilter(filters.SearchFilter):

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        try:
            params = json.loads(request.query_params.get(self.search_param, ''))
        except (TypeError, ValueError):
            return []
        else:
            return params.replace(',', ' ').split()


class GoodsFilter(filters.FilterSet):
    name = django_filters.MethodFilter(action='filter_name')
    category = django_filters.CharFilter()
    price = django_filters.RangeFilter()

    def filter_name(self, queryset, value):
        print value
        query = Q(name__contains=value)
        return queryset.filter(query)

    class Meta:
        model = Goods
        fields = ['name', 'category', 'price']

# -*- coding: utf-8 -*-
__author__ = 'SimonDM'

from django.db.models import Q
from .models import Goods
import django_filters


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # 过滤字段名为shop_price的商品，过滤方法为大于等于/小于等于，如：过滤出商品价格在100-200之间的所有商品
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr='gte', help_text="最低价格")
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte', help_text="最高价格")
    top_category = django_filters.NumberFilter(name="category", method="top_category_filter", help_text="一级分类名称")
    # 过滤字段name中包含某个字符的，如：过滤出名字包含“牛肉”的商品(这里实际使用rest_framework的filters来实现搜索)
    # name = django_filters.CharFilter(name="name", lookup_expr='icontains')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value)
                               | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']

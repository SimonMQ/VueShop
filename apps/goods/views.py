from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import GoodsFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializers import GoodsSerializer, CategorySerializer, HotSearchsSerializer, BannerSerializer, IndexCategorySerializer
# Create your views here.


# 定制分页功能，可以在settings中设置REST_FRAMEWORK，也可以在views中定制。
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    # 分页参数默认是page，可将其设置成p
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品列表页，分页，过滤，搜索，排序
    retrieve:
        商品详情
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')
    # 限速
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    # 点击数+1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def get_queryset(self):
    #
    #     return Goods.objects.filter(shop_price__gt=100)

    # 继承自ListAPIView之后，此函数已经在该类中定义了，可省略。
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()
    #     goods_serializer = GoodsSerializer(goods, many=True)
    #     return Response(goods_serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotSearchsSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


"""VueShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
import xadmin
from VueShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from goods.views import GoodsListViewSet, CategoryViewSet, HotSearchsViewSet, BannerViewSet, IndexCategoryViewset
from trade.views import ShoppingCartVeiwSet, OrderViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet

# 定制view_set方法,将get绑定到list
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

# 注册router,url
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")
router.register(r'categorys', CategoryViewSet, base_name="categorys")
router.register(r'codes', SmsCodeViewSet, base_name="codes")
router.register(r'hotsearchs', HotSearchsViewSet, base_name="hotsearchs")
router.register(r'users', UserViewSet, base_name="users")
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")  # 用户收藏
router.register(r'messages', LeavingMessageViewSet, base_name="messages")  # 用户留言
router.register(r'address', AddressViewSet, base_name="address")  # 收货地址
router.register(r'shopcarts', ShoppingCartVeiwSet, base_name="shopcarts")  # 购物车
router.register(r'orders', OrderViewSet, base_name="orders")  # 购物车
router.register(r'banners', BannerViewSet, base_name="banners")  # 轮播图
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")  # 首页商品数据


# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls')),
    # DRF的文档，View的说明，字段的help_text影响文档的内容（help_text在models、serializer、filter都可以使用）。
    url(r'docs/', include_docs_urls(title="豌豆鲜生")),

    path('ueditor/', include('DjangoUeditor.urls')),

    # 商品列表页
    # path('goods/', goods_list, name='goods-list'),

    url(r'^', include(router.urls)),

    # DRF自带的token认证，可以给注册的user自动生成一个token。
    # 由于我们这里是前后端分离，所以django的csrf_token先摒弃。
    # 这里使用DRF的TokenAuthentication功能
    url(r'^api-token-auth/', views.obtain_auth_token),

    # JWT(JSON WEB TOKEN)认证接口
    url(r'^login/', obtain_jwt_token),
]

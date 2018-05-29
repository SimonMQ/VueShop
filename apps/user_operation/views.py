from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        用户查看收藏详情
    list:
        用户查看收藏列表
    create:
        用户添加收藏
    delete:
        用户删除收藏
    """
    # queryset = UserFav.objects.all()
    # 权限设置：需要认证登录，并且用户请求POST、DELETE等不安全的方法必须是属于自己的对象
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # serializer_class = UserFavSerializer
    def get_serializer_class(self):
        """
        用户收藏页需要使用UserFavDetailSerializer类
        """
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    # 认证方法
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 详情页查找对象的字段：根据goods_id查找
    lookup_field = "goods_id"

    # 用户只能获取属于它的对象列表
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 收藏数+1
    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    # 收藏数-1
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -= 1
        if goods.fav_num < 0:
            goods.fav_num = 0
        goods.save()
        instance.delete()


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 用户只能获取属于它的对象列表
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


# mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
# 这里的增删改查都用到了，所以我们可以直接使用ModelViewSet
class AddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 用户只能获取属于它的对象列表
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

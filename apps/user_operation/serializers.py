# -*- coding: utf-8 -*-
__author__ = 'SimonDM'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏功能，由于客户端用户收藏的时候user是自动配置的，不需要手动填写，所以这里利用HiddenField字段的自动生成功能
    validators字段：
        由于每个用户对每个商品只能收藏一次，即user-goods是唯一的，所以这里用到validators的UniqueTogetherValidator，来对unique_together模型进行约束.
        此方法与models.py中的unique_together字段一致，且message可覆盖错误信息。
    另外，删除字段的时候需要用到id，http://127.0.0.1:8000/userfavs/：ID，Delete方法即可删除某收藏
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        model = UserFav
        fields = ('user', 'goods', 'id')


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 导入留言的添加时间字段，将其设置只读属性
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 导入留言的添加时间字段，将其设置只读属性
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "district", "address", "signer_name", "signer_mobile", "id", "add_time")

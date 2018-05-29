# -*- coding: utf-8 -*-
__author__ = 'SimonDM'

import time
from random import Random
from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label="数量",
                                    error_messages={
                                        "min_value": "商品数量不能小于一个",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    # 由于我们此处继承的是Serializer而不是ModelSerializer，所以必须重写update方法。
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("user", "goods", "nums", "id", "add_time")


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 修改订单的字段，让用户只读
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def generate_order_sn(self):
        # 根据时间、用户id、随机数生成订单号
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id, ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # 调用序列化时生成订单号，并更新保存数据
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"



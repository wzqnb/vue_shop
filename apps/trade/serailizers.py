import time
from trade.models import *
from rest_framework import serializers
from goods.serializers import GoodsSerializer
from goods.models import Goods


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods=GoodsSerializer(many=False,read_only=True)
    class Meta:
        model=ShoppingCart
        fields=("goods","num")


class ShopCartSerializer(serializers.Serializer):
    user=serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums=serializers.IntegerField(required=True,label="数量",min_value=1,error_messages={
        "required":"请选择购买数量",
        "min_value":"购买数量不能少于1"
    })
    goods=serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self, validated_data):
        user=self.context["request"].user
        nums=validated_data["nums"]
        goods=validated_data["goods"]

        existed=ShoppingCart.objects.filter(user=user,goods=goods)

        if existed:
            existed=existed[0]
            existed.nums+=nums
            existed.save()
        else:
            ShoppingCart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nums=validated_data["nums"]
        instance.save()
        return instance

class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)


    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    # def validate(self, attrs):
    #     attrs["order_sn"] = self.generate_order_sn()
    #     return attrs
    def validate(self, attrs):
        attrs["order_sn"]=self.generate_order_sn()
        return attrs
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    # 一个订单有多个订单商品项
    goods = OrderGoodsSerialzier(many=True)



    class Meta:
        model = OrderInfo
        fields = "__all__"



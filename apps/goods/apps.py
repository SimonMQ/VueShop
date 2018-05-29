from django.apps import AppConfig


class GoodsConfig(AppConfig):
    name = 'goods'
    # 修改xadmin后台左侧导航栏的goods显示方式
    verbose_name = "商品"

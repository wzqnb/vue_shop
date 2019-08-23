"""myshopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
import xadmin
from django.urls import path, re_path, include
from django.views.static import serve
from myshopping.settings import MEDIA_ROOT
from rest_framework.authtoken import views

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from goods.views import GoodsListViewSet, CategoryViewset
# from trade.views import ShoppingCartViewset, OrderViewset
from user_operation.views import UserFavViewset
from users.views import SmsCodeViewset, UserViewset
router=DefaultRouter()
# 配置goods的url,这个basename是干啥的
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置Category的url
router.register(r'categories', CategoryViewset, base_name="categories")

# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")

# 配置users的url
router.register(r'users', UserViewset, base_name="users")

# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
# 热搜词
# router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 引入xadmin
    path('ueditor/', include('DjangoUeditor.urls')),
    # 引入djangoUeditor
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 调试登录
    path('api-auth/', include('rest_framework.urls')),
    # drf自带的token授权登录,获取token需要向该地址post数据
    path('api-token-auth/', views.obtain_auth_token),

    # jwt的token认证
    path('login/', obtain_jwt_token),
    # router的path路径
    re_path('^', include(router.urls)),

]

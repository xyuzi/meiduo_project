from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import home, user, image, sku, orders, spu, specs, options, channel

urlpatterns = [
    re_path(r'^authorizations/$', obtain_jwt_token),
    re_path(r'^statistical/total_count/$', home.PeopleCountViwe.as_view()),
    re_path(r'^statistical/day_active/$', home.PeopleLastCountView.as_view()),
    re_path(r'^statistical/day_orders/$', home.PeopleOrderInfoCountView.as_view()),
    re_path(r'^statistical/month_increment/$', home.PeopleMonthCountView.as_view()),
    re_path(r'^users/$', user.SelectUserInfoView.as_view()),
    re_path(r'^skus/simple/$', sku.SKUInfoView.as_view()),
    re_path(r'^goods/simple/$', sku.GoodsSimpleView.as_view()),
    re_path(r'^goods/(?P<pk>\d+)/specs/$', sku.GoodsSpecificationView.as_view()),
    re_path(r'^orders/$', orders.OrdersInfoView.as_view()),
    re_path(r'^orders/(?P<pk>\d+)/$', orders.OrdersInforMationView.as_view()),
    re_path(r'^orders/(?P<order_id>\d+)/status/$', orders.OrdersStatusView.as_view()),
    re_path(r'^goods/brands/simple/$', spu.GoodsBrandInfoView.as_view()),
    re_path(r'^goods/channel/categories/$', spu.GoodsCategoriesOneInfoView.as_view()),
    re_path(r'^goods/channel/categories/(?P<pk>\d+)/$', spu.GoodsCategoriesInfoView.as_view()),
    re_path(r'^goods/channel_types/$', channel.ChannelGroupView.as_view()),
    re_path(r'^goods/categories/$', channel.ChannelCategoriesView.as_view()),
]

routers = DefaultRouter()
# routers = SimpleRouter()

routers.register('skus/images', image.SKUImageView, basename='SKU')
routers.register('skus', sku.SKUView, basename='skus')
routers.register('goods/channels', channel.ChannelInfoView, basename='channel')
routers.register('goods/specs', specs.SpecsInfoView, basename='specs')
routers.register('goods', spu.GoodsInfoView, basename='goods')
routers.register('specs/options', options.OptionsInfoView, basename='options')

urlpatterns += routers.urls

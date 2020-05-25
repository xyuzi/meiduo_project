from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import home, user, image, sku

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
]

routers = DefaultRouter()

routers.register('skus/images', image.SKUImageView, basename='SKU')
routers.register('skus', sku.SKUView, basename='skus')
urlpatterns += routers.urls

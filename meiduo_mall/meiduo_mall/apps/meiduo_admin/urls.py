from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^qq/authorization/$', views.QqUrlView.as_view()),
    re_path(r'^oauth_callback/$', views.QqUrlSecondView.as_view()),
]

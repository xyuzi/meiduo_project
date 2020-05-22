from django.urls import re_path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    re_path(r'^authorizations/$', obtain_jwt_token)
]

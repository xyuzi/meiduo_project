from django.shortcuts import render
from django.views import View

# Create your views here.
from users.models import User
from django.http import JsonResponse


class UsernameCountView(View):

    def get(self, request, username):
        '''接受用户名,判断是否存在'''

        # 访问数据库
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据库失败'
            })

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'count': count
        })

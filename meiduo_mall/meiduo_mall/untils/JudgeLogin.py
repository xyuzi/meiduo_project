from django.http import JsonResponse


def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'code': 400,
                'errmsg': '请先登录'
            })

    return wrapper


class LoginMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return my_decorator(view)

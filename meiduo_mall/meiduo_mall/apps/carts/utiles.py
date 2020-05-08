import base64
import pickle

from django_redis import get_redis_connection


def merage_cookie(request, response):
    """合并cookie ==> redis"""
    cookie_data = request.COOKIES.get('carts')

    if not cookie_data:
        return response

    cart_dict = pickle.loads(base64.b64decode(cookie_data))

    new_dict = {}
    new_add = []
    new_remove = []

    for sku_id, dict in cart_dict.items():
        new_dict[sku_id] = dict['count']

        if dict['selected']:
            new_add.append(sku_id)
        else:
            new_remove.append(sku_id)

    redis_conn = get_redis_connection('carts')
    redis_conn.hmset('carts_%s' % request.user.id, new_dict)

    if new_add:
        redis_conn.sadd('selected_%s' % request.user.id, *new_add)
    else:
        redis_conn.srem('selected_%s' % request.user.id, *new_remove)

    response.delete_cookie('carts')

    return response

import json
import re

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.views import View

# Create your views here.
from carts.utiles import merage_cookie
from goods.models import SKU
from meiduo_mall.utils.JudgeLogin import LoginMixin
from users.models import User, Address
from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection
from celery_tasks.email.tasks import send_verify_email
import logging

logger = logging.getLogger('django')


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


class MobileCountView(View):
    '''手机号重复验证'''

    def get(self, request, mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
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


class RegisterView(View):
    def post(self, request):
        '''注册接口'''
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        sms_code_client = dict.get('sms_code')
        allow = dict.get('allow')

        if not all([username, password, password2, mobile, sms_code_client, allow]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({
                'code': 400,
                'errmsg': '用户名格式不正确'
            })
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码格式不正确'
            })
        if password2 != password:
            return JsonResponse({
                'code': 400,
                'errmsg': '两次输入密码不匹配'
            })
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '手机号码格式不正确'
            })
        if not allow:
            return JsonResponse({
                'code': 400,
                'errmsg': '未勾选条款'
            })
        redis_coon = get_redis_connection('verify_code')
        try:
            sms_code_server = redis_coon.get('sms_%s' % mobile)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据库失败'
            })
        if not sms_code_server:
            return JsonResponse({
                'code': 400,
                'errmsg': '短信验证码过期'
            })
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({
                'code': 400,
                'errmsg': '验证码不匹配'
            })

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '存入数据库失败'
            })
        login(request, user)
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        response = merage_cookie(request, response)
        return response


class LoginView(View):
    '''登录接口'''

    def post(self, request):
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')

        if not all([username, password]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必穿参数'
            })
        user = authenticate(username=username,
                            password=password)
        if user is None:
            return JsonResponse({'code': 400,
                                 'errmsg': '用户名或者密码错误'})
        login(request, user)
        # 勾选后会判断让cookis里面username一起消失或出现
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        if remembered is False:
            request.session.set_expiry(0)
            response.set_cookie('username', user.username, max_age=None)
        else:
            request.session.set_expiry(None)
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        response = merage_cookie(request, response)

        return response


class LogoutView(View):
    def delete(self, request):
        logout(request)
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        response.delete_cookie('username')
        return response


class UserInfoView(LoginMixin, View):
    def get(self, request):
        dict = {
            "username": request.user.username,
            "mobile": request.user.mobile,
            "email": request.user.email,
            "email_active": request.user.email_active
        }

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'info_data': dict
        })


class EmailView(LoginMixin, View):
    def put(self, request):
        dict = json.loads(request.body.decode())
        email = dict.get('email')
        if not email:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({
                'code': 400,
                'errmsg': '邮箱格式不正确'
            })

        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '保持邮箱信息失败'
            })
        url = request.user.generate_verify_email_url()
        # 发送邮件给email 异步执行
        # send_verify_email.delay(email, '邮箱验证链接')
        email = '<' + email + '>'
        send_verify_email.delay(email, url)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


class VerifyEmailView(View):
    def put(self, request):
        token = request.GET.get('token')

        if not token:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        user = User.check_verify_email_token(token)
        if not user:
            return JsonResponse({
                'code': 400,
                'errmsg': '无效的token'
            })

        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '激活失败'
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


class CreateAddressView(LoginMixin, View):
    def post(self, request):
        try:
            count = Address.objects.filter(user=request.user,
                                           is_delete=False).count()
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据库出错'
            })
        if count > 20:
            return JsonResponse({
                'code': 400,
                'errmsg': '超过地址存储数量上限'
            })

        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        tel = dict.get('tel')
        email = dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '传入mobile格式有误'
            })

        if tel:
            if re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '传入tel格式有误'
                })

        if email:
            if re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '传入email格式有误'
                })

        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '存入数据失败'
            })

        # address_dict = {
        #     'id': address.id,
        #     'title': address.title,
        #     'receiver': address.receiver,
        #     'province': address.province.name,
        #     'city': address.city.name,
        #     'district': address.district.name,
        #     'place': address.place,
        #     'mobile': address.mobile,
        #     'tel': address.tel,
        #     'email': address.email
        # }
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            # 'address': address_dict
        })


class AddressView(LoginMixin, View):
    def get(self, request):
        try:
            addresses = Address.objects.filter(user=request.user,
                                               is_delete=False)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据库失败',
            })
        address_list = []

        for address in addresses:
            address_dict = {
                'id': address.id,
                'title': address.title,
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email
            }

            default_address = request.user.default_address
            if default_address.id == address.id:
                address_list.insert(0, address_dict)
            else:
                address_list.append(address_dict)

        default_id = request.user.default_address_id
        return JsonResponse({
            'code': 400,
            'errmsg': 'ok',
            'default_address_id': default_id,
            'addresses': address_list
        })


class UpdateDestroyAddressView(LoginMixin, View):
    def put(self, request, address_id):
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        tel = dict.get('tel')
        email = dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '传入mobile格式有误'
            })

        if tel:
            if re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '传入tel格式有误'
                })

        if email:
            if re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '传入email格式有误'
                })

        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
            address = Address.objects.get(id=address_id)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '更新地址失败'
            })

        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'address': address_dict
        })

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            address.is_delete = True
            address.save()
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '数据修改失败',
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
        })


class DefaultAddressView(LoginMixin, View):
    def put(self, request, address_id):
        try:
            request.user.default_address_id = address_id
            request.user.save()
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '保存数据失败'
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


class UpdateTitleAddressView(LoginMixin, View):
    def put(self, request, address_id):
        title_dict = json.loads(request.body.decode())
        title = title_dict.get('title')
        if not title:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })
        try:
            address = Address.objects.get(id=address_id)
            address.title = title
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '保存数据失败'
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


class ChangePasswordView(LoginMixin, View):
    def put(self, request):
        password_dict = json.loads(request.body.decode())
        old_password = password_dict.get('old_password')
        new_password = password_dict.get('new_password')
        new_password2 = password_dict.get('new_password2')

        if not all([old_password, new_password, new_password2]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not request.user.check_password(old_password):
            return JsonResponse({
                'code': 400,
                'errmsg': '原始密码不正确'
            })

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', new_password):
            return JsonResponse({
                'code': 400,
                'errmsg': '修改密码格式错误'
            })

        if new_password != new_password2:
            return JsonResponse({
                'code': 400,
                'errmsg': '两次密码输入不一致'
            })
        if new_password == old_password:
            return JsonResponse({
                'code': 400,
                'errmsg': '新密码与旧密码一致'
            })
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '修改密码失败'
            })
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        logout(request)
        response.delete_cookie('username')
        return response


class UserHistoryView(LoginMixin, View):
    """用户浏览记录"""

    def post(self, request):
        """保存用户浏览记录"""
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400,
                                 'errmsg': '数据错误'})

        redis_conn = get_redis_connection('history')
        pl = redis_conn.pipeline()

        pl.lrem('history_%s' % request.user.id, 0, sku_id)
        pl.lpush('history_%s' % request.user.id, sku_id)
        pl.ltrim('history_%s' % request.user.id, 0, 4)

        pl.execute()

        return JsonResponse({'code': 0,
                             'errmsg': 'OK'})

    def get(self, request):
        """展示浏览记录"""
        redis_coon = get_redis_connection('history')
        sku_ids = redis_coon.lrange('history_%s' % request.user.id, 0, -1)
        list = []
        for sku_id in sku_ids:
            try:
                sku = SKU.objects.get(id=sku_id)
            except Exception  as e:
                return JsonResponse({
                    'code': 400,
                    'errmsg': '访问数据出错'
                })
            list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'price': sku.price
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'skus': list
        })

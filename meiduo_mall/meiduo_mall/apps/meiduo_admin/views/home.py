from django.db.models.functions import datetime
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from goods.models import GoodsVisitCount
from users.models import User
from datetime import date, timedelta


class PeopleCountViwe(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = User.objects.all().count()
        now = date.today()
        return Response({
            'count': count,
            'date': now
        })


class PeopleLastCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = date.today()
        count = User.objects.filter(last_login__gte=now).count()

        return Response({
            'count': count,
            'date': now
        })


class PeopleOrderInfoCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = date.today()
        count = User.objects.filter(orderinfo__create_time__gte=now).distinct().count()

        return Response({
            'count': count,
            'date': now
        })


class PeopleMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = date.today()
        last_month = now - timedelta(days=30)

        list = []

        for i in range(30):
            day = last_month + timedelta(days=i)
            day_tomorrow = last_month + timedelta(days=i + 1)

            count = User.objects.filter(date_joined__gte=day, date_joined__lt=day_tomorrow).count()

            list.append({
                'count': count,
                'date': day
            })

        return Response(list)


class PeopleDayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        day = date.today()
        day_tomorrow = day + timedelta(days=1)

        count = User.objects.filter(date_joined__gte=day, date_joined__lt=day_tomorrow).count()

        return Response({
            'count': count,
            'date': day
        })


class PeopleGoodsDayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        goods = GoodsVisitCount.objects.all()

        list = []

        for good in goods:
            list.append({'category': good.category.name, 'count': good.count})

        return Response(list)
# Generated by Django 2.2.5 on 2020-05-26 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_auto_20200526_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodschannel',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsChannelGroup', verbose_name='组号'),
        ),
    ]

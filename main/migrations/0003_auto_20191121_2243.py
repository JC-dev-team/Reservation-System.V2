# Generated by Django 2.2.6 on 2019-11-21 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191121_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='prod_desc',
        ),
        migrations.RemoveField(
            model_name='production',
            name='prod_img',
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-29 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musictest', '0009_auto_20200729_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='keyword',
        ),
    ]

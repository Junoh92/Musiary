# Generated by Django 3.0.8 on 2020-07-15 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musictest', '0006_post_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='musictest'),
        ),
    ]

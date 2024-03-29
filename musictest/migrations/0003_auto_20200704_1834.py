# Generated by Django 3.0.8 on 2020-07-04 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musictest', '0002_remove_post_music'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='music',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='singer',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=20),
        ),
    ]

# Generated by Django 3.0.8 on 2020-08-02 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musictest', '0012_auto_20200731_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='albumart_link',
        ),
        migrations.RemoveField(
            model_name='post',
            name='music',
        ),
        migrations.RemoveField(
            model_name='post',
            name='singer',
        ),
        migrations.RemoveField(
            model_name='post',
            name='song',
        ),
        migrations.AddField(
            model_name='post',
            name='song_official',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-07 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_enabled',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 2.2 on 2020-03-08 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='user',
            field=models.ForeignKey(on_delete=True, related_name='tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]

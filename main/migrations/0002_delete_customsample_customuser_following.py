# Generated by Django 4.2.13 on 2024-05-18 17:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomSample',
        ),
        migrations.AddField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]

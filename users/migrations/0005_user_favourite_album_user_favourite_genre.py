# Generated by Django 4.2 on 2023-04-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_album',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='favourite_genre',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
# Generated by Django 4.2 on 2023-04-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_alter_record_album'),
        ('users', '0002_alter_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='collection',
            field=models.ManyToManyField(blank=True, related_name='record_collection', to='records.record'),
        ),
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='record_wishlist', to='records.record'),
        ),
    ]

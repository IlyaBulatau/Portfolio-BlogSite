# Generated by Django 4.2.7 on 2023-11-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, height_field=240, upload_to='avatars/', width_field=300),
        ),
    ]

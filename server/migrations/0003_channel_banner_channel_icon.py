# Generated by Django 4.2.7 on 2023-11-19 12:49

from django.db import migrations, models
import server.models
import server.validators


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=server.models.server_banner),
        ),
        migrations.AddField(
            model_name='channel',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=server.models.server_icon, validators=[server.validators.validate_icon_size, server.validators.validate_image_file_exstension]),
        ),
    ]

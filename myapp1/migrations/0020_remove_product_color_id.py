# Generated by Django 3.1.7 on 2021-04-07 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0019_auto_20210407_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color_id',
        ),
    ]

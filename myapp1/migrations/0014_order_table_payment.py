# Generated by Django 3.1.7 on 2021-03-23 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0013_auto_20210323_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_table',
            name='payment',
            field=models.BooleanField(default=False),
        ),
    ]
